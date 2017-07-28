from enum import IntEnum

N_ADMIN = 'national_admin'
N_MOD = 'national_moderator'
N_USER = 'national_user'
R_ADMIN = 'regional_admin'
R_MOD = 'regional_moderator'
R_USER = 'regional_user'
ALL_ROLES = [N_ADMIN, N_MOD, N_USER, R_ADMIN, R_MOD, R_USER]
ONLY_ADMIN_ROLE = [N_ADMIN, R_ADMIN]
ADMIN_MOD_ROLE = [N_ADMIN, R_ADMIN, N_MOD, R_MOD]

MODAL_ADD_ID = 'modal-add'
MODAL_DEL_ID = 'modal-delete'
MODAL_EDIT_ID = 'modal-edit'
BTNADD_ID = 'addBtn'
BTNEDIT_ID = 'editBtn'
BTNDEL_ID = 'delBtn'

SELECT_DEFAULT_ID = 'pgs_select'


class GenderType(IntEnum):
    male = 1  # nam
    female = 2  # nu


class FarmerType(IntEnum):
    member = 1  # thanh vien
    reviewer = 2  # thanh tra


class CertificateStatusType(IntEnum):
    approve = 1  # dong y cap
    reject = 2  # tu choi cap
    in_conversion = 3  # chua xac nhan
    approve_no_cert = 4  # khong co chung chi


class CertificateReVerifyStatusType(IntEnum):
    not_check = 1  # chua thanh tra
    valid = 2  # ok
    decline = 3  # thu hoi
    warning = 4  # canh cao
    punish = 5  # dinh chi, xu phat
