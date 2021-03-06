from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, SelectField, \
    HiddenField, validators, SubmitField

from pgscm import const as c
from pgscm.utils import __, Select, Submit, Date

data_required = validators.DataRequired(message=__('Required field!'))


class CertificateForm(FlaskForm):
    certificate_code = StringField(
        __('Certificate code'), validators=[],
        render_kw={"placeholder": __('Certificate code')})
    group_area = IntegerField(
        __('Group area'), validators=[data_required],
        render_kw={"placeholder": __('Group area')})
    member_count = IntegerField(
        __('Member count'), validators=[data_required],
        render_kw={"placeholder": __('Member count')})
    certificate_start_date = DateField(
        __('Certificate verify date'), widget=Date(),
        render_kw={"placeholder": __('Certificate verify date')})
    gov_certificate_id = StringField(
        __('Decision code'),
        validators=[data_required],
        render_kw={"placeholder": __('Decision code')})
    certificate_expiry_date = DateField(
        __('Certificate expiry date'), validators=(validators.Optional(),),
        widget=Date(),
        render_kw={"placeholder": __('Certificate expiry date')})
    status = SelectField(
        __('Status'), validators=[data_required], coerce=int, widget=Select(),
        choices=[(c.CertificateStatusType.approved.value, __('Approved')),
                 (c.CertificateStatusType.rejected.value, __('Refuse')),
                 (c.CertificateStatusType.decline.value,
                  __('Withdraw')),
                 (c.CertificateStatusType.warning.value,
                  __('Warning')),
                 (c.CertificateStatusType.punish.value,
                  __('Punish'))])
    re_verify_status = SelectField(
        __('Reverify Status'), validators=[data_required], coerce=int,
        widget=Select(),
        choices=[(c.CertificateReVerifyStatusType.adding.value,
                  __('New')),
                 (c.CertificateReVerifyStatusType.keeping.value,
                  __('Remaining')),
                 (c.CertificateReVerifyStatusType.converting.value,
                  __('Conversion')),
                 (c.CertificateReVerifyStatusType.fortuity.value,
                  __('Suddenly'))])
    owner_farmer_id = SelectField(__('Certificated farmer'), validators=[
        data_required], coerce=str, widget=Select(), id='load_now-farmer')
    owner_group_id = SelectField(__('Certificated group'), validators=[
        data_required], coerce=str, widget=Select(), id='load_now-group')
    modify_info = StringField(__('Note'),
                              render_kw={"placeholder": __('Note')})
    id = HiddenField(__('Id'), validators=[data_required])
    submit = SubmitField(__('Submit'), widget=Submit())
