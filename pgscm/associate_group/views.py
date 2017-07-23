from flask import render_template
from flask_security import roles_accepted, current_user

from . import agroup

from pgscm.db import models
from pgscm import const as c


@agroup.route('/vi/lien-nhom', endpoint='index_vi')
@agroup.route('/en/associate-group', endpoint='index_en')
@roles_accepted(c.N_ADMIN, c.R_ADMIN, c.R_MOD, c.N_MOD, c.N_USER)
def index():
    ags = models.AssociateGroup.query.filter_by(
        province_id=current_user.province_id).all()
    return render_template('agroup/index.html', ags=ags)
