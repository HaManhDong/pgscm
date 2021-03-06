import uuid

from flask import render_template, current_app, request, \
    flash, redirect, url_for, jsonify
from flask_security import roles_accepted, current_user
from sqlalchemy import func

from . import group
from .forms import GroupForm

from pgscm import sqla
from pgscm.db import models
from pgscm.utils import __, DeleteForm, check_role, is_region_role, soft_delete
from pgscm import const as c

crud_role = c.ADMIN_MOD_ROLE


@group.route('/vi/nhom', endpoint='index_vi', methods=['GET', 'POST'])
@group.route('/en/group', endpoint='index_en', methods=['GET', 'POST'])
@roles_accepted(*c.ALL_ROLES)
def index():
    form = GroupForm()
    dform = DeleteForm()
    if current_app.config['AJAX_CALL_ENABLED']:
        form.associate_group_id.choices = []
        form.ward_id.choices = []
        form.district_id.choices = []
        form.province_id.choices = []
        associate_group_id = current_user.associate_group_id
        if associate_group_id and is_region_role():
            form.associate_group_id.choices = [
                (ag.id, ag.name) for ag in
                models.AssociateGroup.query.filter_by(
                    id=associate_group_id).all()]
        return render_template('group/index.html', form=form, dform=dform)
    else:
        province_id = current_user.province_id
        if province_id and is_region_role():
            gs = models.Group.query.filter_by(
                province_id=province_id, _deleted_at=None).all()
            form.associate_group_id.choices = [(
                ag.id, ag.name) for ag in
                models.AssociateGroup.query.filter_by(
                    province_id=province_id,
                    _deleted_at=None).order_by(
                    models.AssociateGroup.name.asc()).all()]
            form.province_id.choices = [
                (p.province_id, p.type + " " + p.name) for p in
                models.Province.query.filter_by(
                    province_id=province_id).order_by(
                    models.Province.name.asc()).all()]
            form.district_id.choices = [
                (d.district_id, d.type + " " + d.name) for d in
                models.District.query.filter_by(
                    province_id=province_id).order_by(
                    models.District.name.asc()).all()]
            form.ward_id.choices = [
                (w.ward_id, w.type + " " + w.name) for w in
                models.Ward.query.join(models.District).filter(
                    models.District.province_id == province_id).order_by(
                    models.Ward.name.asc()).all()]
        else:
            gs = models.Group.query.filter_by(_deleted_at=None).all()
            form.associate_group_id.choices = []
            form.province_id.choices = []
            form.district_id.choices = []
            form.ward_id.choices = []

        # form create or edit submit
        if request.method == 'POST' and form.data['submit']:
            if not check_role(crud_role):
                return redirect(url_for(request.endpoint))
            form.province_id.choices = [(form.province_id.data,
                                         form.province_id.label.text)]
            form.district_id.choices = [(form.district_id.data,
                                         form.district_id.label.text)]
            form.ward_id.choices = [(form.ward_id.data,
                                     form.ward_id.label.text)]
            form.associate_group_id.choices = [
                (form.associate_group_id.data,
                 form.associate_group_id.label.text)]
            # edit group
            if form.id.data:
                if form.validate_on_submit():
                    edit_group = sqla.session.query(models.Group) \
                        .filter_by(id=form.id.data).one()
                    edit_group.group_code = form.group_code.data
                    edit_group.name = form.name.data
                    edit_group.village = form.village.data
                    if edit_group.associate_group_id != \
                            form.associate_group_id.data:
                        edit_group.associate_group = sqla.session \
                            .query(models.AssociateGroup) \
                            .filter_by(id=form.associate_group_id.data).one()
                    if edit_group.province_id != form.province_id.data:
                        edit_group.province = sqla.session \
                            .query(models.Province) \
                            .filter_by(province_id=form.province_id.data).one()
                    if edit_group.district_id != form.district_id.data:
                        edit_group.district = sqla.session \
                            .query(models.District) \
                            .filter_by(district_id=form.district_id.data).one()
                    if edit_group.ward_id != form.ward_id.data:
                        edit_group.ward = sqla.session.query(models.Ward) \
                            .filter_by(ward_id=form.ward_id.data).one()
                    sqla.session.commit()
                    for gr in gs:
                        if gr.id == edit_group.id:
                            gs.remove(gr)
                            gs.append(edit_group)
                    flash(str(__('Update group success!')), 'success')
                    return redirect(url_for(request.endpoint))
                else:
                    flash(str(__('The form is not validated!')), 'error')

            # add group
            else:
                form.id.data = str(uuid.uuid4())
                if form.validate_on_submit():
                    associate_group = sqla.session.query(
                        models.AssociateGroup) \
                        .filter_by(id=form.associate_group_id.data).one()
                    province = sqla.session.query(models.Province) \
                        .filter_by(province_id=form.province_id.data).one()
                    district = sqla.session.query(models.District) \
                        .filter_by(district_id=form.district_id.data).one()
                    ward = sqla.session.query(models.Ward) \
                        .filter_by(ward_id=form.ward_id.data).one()
                    new_group = models.Group(
                        id=form.id.data,
                        group_code=form.group_code.data,
                        name=form.name.data, village=form.village.data,
                        ward=ward, district=district,
                        associate_group=associate_group,
                        province=province)
                    sqla.session.add(new_group)
                    sqla.session.commit()
                    gs.append(new_group)
                    flash(str(__('Add group success!')), 'success')
                    return redirect(url_for(request.endpoint))
                else:
                    flash(str(__('The form is not validated!')), 'error')

        # form delete submit
        if request.method == 'POST' and dform.data['submit_del']:
            if not check_role(crud_role):
                return redirect(url_for(request.endpoint))
            elif dform.validate_on_submit():
                del_group = sqla.session.query(models.Group) \
                    .filter_by(id=dform.id.data).one()
                del_group._deleted_at = func.now()
                if dform.modify_info.data:
                    del_group._modify_info = dform.modify_info.data
                sqla.session.commit()
                flash(str(__('Delete group success!')), 'success')
                return redirect(url_for(request.endpoint))

        return render_template('group/index.html', gs=gs,
                               form=form, dform=dform)


def add_value_for_select_field(form):
    form.province_id.choices = [(form.province_id.data,
                                 form.province_id.label.text)]
    form.district_id.choices = [(form.district_id.data,
                                 form.district_id.label.text)]
    form.ward_id.choices = [(form.ward_id.data,
                             form.ward_id.label.text)]
    form.associate_group_id.choices = [(form.associate_group_id.data,
                                        form.associate_group_id.label.text)]


@group.route('/vi/them-nhom', endpoint='add_group_vi', methods=['POST'])
@group.route('/en/add-group', endpoint='add_group_en', methods=['POST'])
@roles_accepted(*c.ADMIN_MOD_ROLE)
def add_group():
    form = GroupForm()
    form.id.data = str(uuid.uuid4())
    add_value_for_select_field(form)
    if form.validate_on_submit():
        associate_group = sqla.session.query(
            models.AssociateGroup) \
            .filter_by(id=form.associate_group_id.data).one()
        province = sqla.session.query(models.Province) \
            .filter_by(province_id=form.province_id.data).one()
        district = sqla.session.query(models.District) \
            .filter_by(district_id=form.district_id.data).one()
        ward = sqla.session.query(models.Ward) \
            .filter_by(ward_id=form.ward_id.data).one()
        new_group = models.Group(
            id=form.id.data,
            group_code=form.group_code.data,
            name=form.name.data, village=form.village.data,
            ward=ward, district=district,
            associate_group=associate_group,
            province=province,
            created_at=form.created_at.data)
        sqla.session.add(new_group)
        sqla.session.commit()
        return jsonify(is_success=True, message=str(__('Add group success!')))
    else:
        return jsonify(is_success=False,
                       message=str(__('The form is not validate!')))


@group.route('/vi/sua-nhom', endpoint='edit_group_vi', methods=['PUT'])
@group.route('/en/edit-group', endpoint='edit_group_en', methods=['PUT'])
@roles_accepted(*c.ADMIN_MOD_ROLE)
def edit_group():
    form = GroupForm()
    add_value_for_select_field(form)
    if form.validate_on_submit():
        edit_group = sqla.session.query(models.Group) \
            .filter_by(id=form.id.data).one()
        edit_group.group_code = form.group_code.data
        edit_group.name = form.name.data
        edit_group.village = form.village.data
        edit_group.created_at = form.created_at.data
        if edit_group.associate_group_id != \
                form.associate_group_id.data:
            edit_group.associate_group = sqla.session \
                .query(models.AssociateGroup) \
                .filter_by(id=form.associate_group_id.data).one()
        if edit_group.province_id != form.province_id.data:
            edit_group.province = sqla.session \
                .query(models.Province) \
                .filter_by(province_id=form.province_id.data).one()
        if edit_group.district_id != form.district_id.data:
            edit_group.district = sqla.session \
                .query(models.District) \
                .filter_by(district_id=form.district_id.data).one()
        if edit_group.ward_id != form.ward_id.data:
            edit_group.ward = sqla.session.query(models.Ward) \
                .filter_by(ward_id=form.ward_id.data).one()
        sqla.session.commit()
        return jsonify(is_success=True, message=str(__('Edit group success!')))
    else:
        return jsonify(is_success=False,
                       message=str(__('The form is not validate!')))


@group.route('/vi/xoa-nhom', endpoint='delete_group_vi', methods=['DELETE'])
@group.route('/en/delete-group', endpoint='delete_group_en',
             methods=['DELETE'])
@roles_accepted(*c.ADMIN_MOD_ROLE)
def delete_group():
    return soft_delete(sqla, "group", models)
