from assemblyline import odm
from assemblyline.common import forge
from assemblyline.common.str_utils import StringTable

Classification = forge.get_classification()


TYPES = StringTable('TYPES', [
    ("admin", 0),
    ("user", 1),
    ("signature_manager", 2),
    ("signature_importer", 3),
    ("viewer", 4),
    ("submitter", 5),
    ("custom", 6),
])

ROLES = StringTable('ROLES', [
    ("alert_manage", 0),
    ("alert_view", 1),
    ("apikey_access", 2),
    ("bundle_download", 3),
    ("file_detail", 4),
    ("file_download", 5),
    ("file_purge", 33),
    ("heuristic_view", 6),
    ("obo_access", 7),
    ("replay_trigger", 8),
    ("safelist_view", 9),
    ("safelist_manage", 10),
    ("signature_download", 11),
    ("signature_view", 12),
    ("submission_create", 13),
    ("submission_delete", 14),
    ("submission_manage", 15),
    ("submission_view", 16),
    ("workflow_manage", 17),
    ("workflow_view", 18),
    ("administration", 19),
    ("replay_system", 20),
    ("signature_import", 21),
    ("signature_manage", 22),
    ("archive_view", 23),
    ("archive_manage", 24),
    ("archive_trigger", 25),
    ("archive_download", 26),
    ("self_manage", 27),
    ("retrohunt_view", 28),
    ("retrohunt_run", 29),
    ("external_query", 30),
    ("badlist_view", 31),
    ("badlist_manage", 32),
    ("archive_comment", 33),
    ("assistant_use", 34),
    ("submission_customize", 35)
])


SCOPES = {"r", "w", "rw", "c"}
USER_TYPES = [
    TYPES.admin,               # Perform administartive task and has access to all roles
    TYPES.user,                # Normal user of the system
    TYPES.signature_manager,   # Super user that also has access to roles for managing signatures in the system
    TYPES.signature_importer,  # Has access to roles for importing signatures in the system
    TYPES.viewer,              # User that can only view the data
    TYPES.submitter,           # User that can only start submissions
    TYPES.custom,              # Has custom roles selected
]

USER_ROLES_BASIC = {
    ROLES.alert_manage,        # Modify labels, priority, status, verdict or owner of alerts
    ROLES.alert_view,          # View alerts in the system
    ROLES.archive_trigger,     # Send Submission, files and results to the archive
    ROLES.archive_view,        # View archived data in the system
    ROLES.archive_manage,      # Modify attributes of archived Submissions/Files/Results
    ROLES.archive_download,    # Download file from the archive
    ROLES.archive_comment,     # Comment on archived files
    ROLES.apikey_access,       # Allow access via API keys
    ROLES.bundle_download,     # Create bundle of a submission
    ROLES.external_query,      # Allow federated searches against external systems
    ROLES.file_detail,         # View files in the file viewer
    ROLES.file_download,       # Download files from the system
    ROLES.heuristic_view,      # View heuristics of the system
    ROLES.obo_access,          # Allow access via On Behalf Off tokens
    ROLES.replay_trigger,      # Allow submission to be replayed on another server
    ROLES.safelist_view,       # View safelist items
    ROLES.safelist_manage,     # Manage (add/delete) safelist items
    ROLES.self_manage,         # Manage currently logged in user settings
    ROLES.signature_download,  # Download signatures from the system
    ROLES.signature_view,      # View signatures
    ROLES.submission_create,   # Create a submission in the system
    ROLES.submission_delete,   # Delete submission from the system
    ROLES.submission_manage,   # Set user verdict on submissions
    ROLES.submission_view,     # View submission's results
    ROLES.workflow_manage,     # Manage (add/delete) workflows
    ROLES.workflow_view,       # View workflows
    ROLES.retrohunt_view,      # View yara searches
    ROLES.retrohunt_run,       # Run yara searches
    ROLES.badlist_view,        # View badlist items
    ROLES.badlist_manage,      # Manage (add/delete) badlist items
    ROLES.submission_customize # Allowed to customize submission properties
}

USER_ROLES = USER_ROLES_BASIC.union({
    ROLES.administration,      # Perform administrative tasks
    ROLES.file_purge,          # Purge files from the filestore
    ROLES.replay_system,       # Manage status of file/submission/alerts during the replay process
    ROLES.signature_import,    # Import signatures in the system
    ROLES.signature_manage,    # Manage signatures sources in the system
    ROLES.assistant_use,       # Use the Assemblyline Assistant
})

USER_TYPE_DEP = {
    TYPES.admin: USER_ROLES,
    TYPES.signature_importer: {
        ROLES.badlist_manage,
        ROLES.safelist_manage,
        ROLES.self_manage,
        ROLES.signature_download,
        ROLES.signature_import,
        ROLES.signature_view
    },
    TYPES.signature_manager: USER_ROLES_BASIC.union({
        ROLES.signature_manage
    }),
    TYPES.user: USER_ROLES_BASIC,
    TYPES.viewer: {
        ROLES.alert_view,
        ROLES.apikey_access,
        ROLES.badlist_view,
        ROLES.file_detail,
        ROLES.obo_access,
        ROLES.heuristic_view,
        ROLES.safelist_view,
        ROLES.self_manage,
        ROLES.signature_view,
        ROLES.submission_view,
        ROLES.workflow_view,
    },
    TYPES.submitter: {
        ROLES.apikey_access,
        ROLES.obo_access,
        ROLES.self_manage,
        ROLES.submission_create,
        ROLES.replay_trigger,
        ROLES.retrohunt_run,
    }
}

ACL_MAP = {
    "R": [
        ROLES.alert_view,
        ROLES.archive_view,
        ROLES.archive_download,
        ROLES.badlist_view,
        ROLES.bundle_download,
        ROLES.external_query,
        ROLES.file_detail,
        ROLES.file_download,
        ROLES.heuristic_view,
        ROLES.safelist_view,
        ROLES.signature_download,
        ROLES.signature_view,
        ROLES.submission_view,
        ROLES.workflow_view,
        ROLES.retrohunt_view,
    ],
    "W": [
        ROLES.alert_manage,
        ROLES.archive_trigger,
        ROLES.archive_manage,
        ROLES.badlist_manage,
        ROLES.replay_trigger,
        ROLES.safelist_manage,
        ROLES.submission_create,
        ROLES.submission_delete,
        ROLES.submission_manage,
        ROLES.submission_customize,
        ROLES.retrohunt_run,
    ],
    "E": [
        ROLES.administration,
        ROLES.apikey_access,
        ROLES.file_purge,
        ROLES.obo_access,
        ROLES.replay_system,
        ROLES.self_manage,
        ROLES.signature_import,
        ROLES.signature_manage,
        ROLES.workflow_manage
    ],
    "C": []
}


def load_roles_form_acls(acls, curRoles):
    # Check if we have current roles first
    if curRoles:
        return curRoles

    # Otherwise load the roles from the api_key ACLs
    roles = set({})
    for acl in ACL_MAP.keys():
        if acl in acls:
            roles = roles.union(ACL_MAP[acl])

    # Return roles as a list
    return list(roles)


def load_roles(types, curRoles):
    # Check if we have current roles first
    if curRoles:
        return curRoles

    # Otherwise load the roles from the user type
    roles = set({})
    for user_type in USER_TYPE_DEP.keys():
        if user_type in types:
            roles = roles.union(USER_TYPE_DEP[user_type])

    # Return roles as a list
    return list(roles)


# This APIKey model can be removed after Assemblyline v4.6
@odm.model(index=False, store=False, description="Model for API keys")
class ApiKey(odm.Model):
    acl = odm.List(odm.Enum(values=ACL_MAP.keys()), description="Access Control List for the API key")
    password = odm.Keyword(description="BCrypt hash of the password for the apikey")
    roles = odm.List(odm.Enum(values=USER_ROLES), default=[], description="List of roles tied to the API key")


@odm.model(index=False, store=False, description="Model of Apps used of OBO (On Behalf Of)")
class Apps(odm.Model):
    client_id = odm.Keyword(description="Username allowed to impersonate the current user")
    netloc = odm.Keyword(description="DNS hostname for the server")
    scope = odm.Enum(values=SCOPES, description="Scope of access for the App token")
    server = odm.Keyword(description="Name of the server that has access")
    roles = odm.List(odm.Enum(values=USER_ROLES), default=[], description="List of roles tied to the App token")


@odm.model(index=True, store=True, description="Model of User")
class User(odm.Model):
    agrees_with_tos = odm.Optional(
        odm.Date(index=False, store=False),
        description="Date the user agree with terms of service")
    api_quota = odm.Optional(odm.Integer(
        store=False, description="Maximum number of concurrent API requests (0: No Quota)"))
    api_daily_quota = odm.Optional(odm.Integer(
        store=False, description="Maximum number of API calls a user can do daily (0: No Quota)"))
    apikeys = odm.Mapping(odm.Compound(ApiKey), default={}, index=False, store=False, description="Mapping of API keys")
    apps = odm.Mapping(odm.Compound(Apps), default={}, index=False, store=False,
                       description="Applications with access to the account")
    can_impersonate = odm.Boolean(default=False, index=False, store=False,
                                  description="Allowed to query on behalf of others?")
    classification = odm.Classification(is_user_classification=True, copyto="__text__",
                                        default=Classification.UNRESTRICTED,
                                        description="Maximum classification for the user")
    dn = odm.Optional(odm.Keyword(store=False, copyto="__text__"), description="User's LDAP DN")
    email = odm.Optional(odm.Email(copyto="__text__"), description="User's email address")
    groups = odm.List(odm.UpperKeyword(), copyto="__text__", default=[],
                      description="List of groups the user submits to")
    identity_id: str = odm.Optional(odm.Keyword(
        store=False, copyto="__text__"),
        description="ID of the matching object in your identity provider (used for logging in as another application)")
    is_active = odm.Boolean(default=True, description="Is the user active?")
    name = odm.Keyword(copyto="__text__", description="Full name of the user")
    otp_sk = odm.Optional(
        odm.Keyword(index=False, store=False),
        description="Secret key to generate one time passwords")
    password = odm.Keyword(index=False, store=False, description="BCrypt hash of the user's password")
    submission_quota = odm.Optional(odm.Integer(store=False,
                                                description="Maximum number of concurrent submissions (0: No Quota)"))
    submission_async_quota = odm.Optional(odm.Integer(
        store=False, description="Maximum number of concurrent async submission (0: No Quota)"))
    submission_daily_quota = odm.Optional(odm.Integer(
        store=False,
        description="Maximum number of submissions a user can do daily (0: No Quota)"))
    type = odm.List(odm.Enum(values=USER_TYPES), default=['user'], description="Type of user")
    roles = odm.List(odm.Enum(values=USER_ROLES), default=[], description="Default roles for user")
    security_tokens = odm.Mapping(odm.Keyword(), index=False, store=False, default={},
                                  description="Map of security tokens")
    uname = odm.Keyword(copyto="__text__", description="Username")
    # can be removed after Assemblyline v4.6
    apikeys = odm.Mapping(odm.Compound(ApiKey), default={},
                        index=False, store=False)
