from collections import namedtuple
from gettext import gettext as _


Error = namedtuple('Error', ['code', 'message', 'required_fields'])
"""
The error named tuple has 4 components:
code: The 7 character uniquely identifying code for this error, 3 A-Z identifying the module
      followed by 4 numeric characters for the msg id.  All general pulp server errors start
      with PLP
message: The message that will be printed for this error
required_files: A list of required fields for printing the message
"""

# The PLP0000 error is to wrap non-pulp exceptions
PLP0000 = Error("PLP0000",
                "%(message)s", ['message'])
PLP0001 = Error("PLP0001",
                _("A general pulp exception occurred"), [])
PLP0002 = Error(
    "PLP0002",
    _("Errors occurred updating bindings on consumers for repo %(repo_id)s and distributor "
      "%(distributor_id)s"),
    ['repo_id', 'distributor_id'])
PLP0003 = Error("PLP0003",
                _("Errors occurred removing bindings on consumers while deleting a distributor for "
                  "repo %(repo_id)s and distributor %(distributor_id)s"),
                ['repo_id', 'distributor_id'])
PLP0004 = Error("PLP0004",
                _("Errors occurred creating bindings for the repository group %(group_id)s.  "
                  "Binding creation was attempted for the repository %(repo_id)s and "
                  "distributor %(distributor_id)s"),
                ['repo_id', 'distributor_id', 'group_id'])

PLP0005 = Error("PLP0005",
                _("Errors occurred deleting bindings for the repository group %(group_id)s.  "
                  "Binding deletion was attempted for the repository %(repo_id)s and "
                  "distributor %(distributor_id)s"),
                ['repo_id', 'distributor_id', 'group_id'])
PLP0006 = Error("PLP0006", _("Errors occurred while updating the distributor configuration for "
                             "repository %(repo_id)s"),
                ['repo_id'])
PLP0007 = Error("PLP0007",
                _("Error occurred while cascading delete of repository %(repo_id)s to distributor "
                  "bindings associated with it."),
                ['repo_id'])
PLP0008 = Error("PLP0008",
                _("Error raising error %(code)s.  "
                  "The field [%(field)s] was not included in the error_data."),
                ['code', 'field'])
PLP0009 = Error("PLP0009", _("Missing resource(s): %(resources)s"), ['resources'])
PLP0010 = Error("PLP0010", _("Conflicting operation reasons: %(reasons)s"), ['reasons'])
PLP0011 = Error("PLP0011", _("Operation timed out after: %(timeout)s"), ['timeout'])
PLP0012 = Error("PLP0012", _("Operation postponed"), [])
PLP0014 = Error("PLP0014", _('Operation not implemented: %(operation_name)s'), ['operation_name'])
PLP0015 = Error("PLP0015", _('Invalid properties: %(properties)s'), ['properties'])
PLP0016 = Error("PLP0016", _('Missing values for: %(properties)s'), ['properties'])
PLP0017 = Error("PLP0017", _('Unsupported properties: %(properties)s'), ['properties'])
PLP0018 = Error("PLP0018", _('Duplicate resource: %(resource_id)s'), ['resource_id'])
PLP0019 = Error("PLP0019", _('Pulp only accepts input encoded in UTF-8: %(value)s'), ['value'])
PLP0020 = Error("PLP0020",
                _("Errors occurred installing content for the consumer group %(group_id)s."),
                ['group_id'])
PLP0021 = Error("PLP0021",
                _("Errors occurred updating content for the consumer group %(group_id)s."),
                ['group_id'])
PLP0022 = Error("PLP0022",
                _("Errors occurred uninstalling content for the consumer group %(group_id)s."),
                ['group_id'])
PLP0023 = Error("PLP0023", _("Task is already in a complete state: %(task_id)s"), ['task_id'])
PLP0024 = Error("PLP0024",
                _("There are no Celery workers found in the system for reserved task work. "
                  "Please ensure that there is at least one Celery worker running, and that the "
                  "celerybeat service is also running."),
                [])
PLP0025 = Error("PLP0025", _("Authentication failed."), [])
PLP0026 = Error(
    "PLP0026", _("Permission denied: user %(user)s cannot perform %(operation)s."),
    ['user', 'operation'])
PLP0027 = Error(
    "PLP0027", _("Authentication with username %(user)s failed: invalid SSL certificate."),
    ['user'])
PLP0028 = Error(
    "PLP0028", _("Authentication with username %(user)s failed: invalid oauth credentials."),
    ['user'])
PLP0029 = Error(
    "PLP0029",
    _("Authentication with username %(user)s failed: preauthenticated remote user is missing."),
    ['user'])
PLP0030 = Error(
    "PLP0030",
    _("Authentication with username %(user)s failed: invalid username or password"), ['user'])
PLP0031 = Error("PLP0031", _("Content source %(id)s could not be found at %(url)s"), ['id', 'url'])
PLP0032 = Error(
    "PLP0032", _("Task %(task_id)s encountered one or more failures during execution."),
    ['task_id'])
PLP0034 = Error("PLP0034", _("The distributor %(distributor_id)s indicated a failed response when "
                             "publishing repository %(repo_id)s."),
                ['distributor_id', 'repo_id'])
PLP0037 = Error(
    "PLP0037",
    _("Content import of %(path)s failed - must be an existing file."),
    ['path'])
PLP0038 = Error("PLP0038", _("The model with id %(model_id)s and class "
                             "%(model_class)s failed to register. Another model has already "
                             "been registered with the same id."), ['model_id', 'model_class'])
PLP0040 = Error("PLP0040", _("Database 'seeds' config must include at least one hostname:port "
                             "value. Refer to /etc/pulp/server.conf for proper use."), [])
PLP0041 = Error("PLP0041", _("Database 'replica_set' config must be specified when more than one "
                             "seed is provided. Refer to /etc/pulp/server.conf for proper use."),
                [])
PLP0042 = Error("PLP0042", _("This request is forbidden."), [])
PLP0043 = Error("PLP0043", _("Database 'write_concern' config can only be 'majority' or 'all'. "
                             "Refer to /etc/pulp/server.conf for proper use."), [])
PLP0044 = Error("PLP0044", _("The target importer does not support the types from the source"), [])
PLP0045 = Error("PLP0045", _("The repository cannot be exported because some units are "
                             "not downloaded."), [])
PLP0046 = Error("PLP0046", _("The repository group cannot be exported because these repos have "
                             "units that are not downloaded: %(repos)s"), ['repos'])
PLP0047 = Error("PLP0047", _("The importer %(importer_id)s indicated a failed response when "
                             "uploading %(unit_type)s unit to repository %(repo_id)s."
                             " Summary: '%(summary)s'. Details: '%(details)s' "),
                ['importer_id', 'unit_type', 'repo_id'])
PLP0048 = Error("PLP0048", _("The file is expected to be present, but is not, for unit %(unit)s"),
                ['unit'])
PLP0049 = Error(
    "PLP0049",
    _('Worker terminated abnormally while processing task %(task_id)s.  '
      'Check the logs for details'),
    ['task_id'])

# Create a section for general validation errors (PLP1000 - PLP2999)
# Validation problems should be reported with a general PLP1000 error with a more specific
# error message nested inside of it.
PLP1000 = Error("PLP1000", _("A validation error occurred."), [])
PLP1001 = Error("PLP1001", _("The consumer %(consumer_id)s does not exist."), ['consumer_id'])
PLP1002 = Error("PLP1002", _("The field %(field)s must have a value specified."), ['field'])
PLP1003 = Error(
    "PLP1003",
    _("The value specified for the field %(field)s must be made up of letters, numbers, "
      "underscores, or hyphens with no spaces."),
    ['field'])
PLP1004 = Error(
    "PLP1004",
    _("An object of type %(type)s already exists in the database with an id of %(object_id)s"),
    ['type', 'object_id'])
PLP1005 = Error("PLP1005", _("The checksum type '%(checksum_type)s' is unknown."),
                ['checksum_type'])
PLP1006 = Error(
    "PLP1006", _("The value specified for the field %(field)s may not start with %(value)s."),
    ['field', 'value'])
PLP1007 = Error("PLP1007", _("The relative path specified must not point outside of the parent"
                             " directory:  %(path)s"), ['path'])
PLP1008 = Error("PLP1008", _("The importer type %(importer_type_id)s does not exist"),
                ['importer_type_id'])
PLP1009 = Error("PLP1009", _("The request body does not contain valid JSON"), [])
PLP1010 = Error("PLP1010", _("Provided value %(value)s for field %(field)s must be of type "
                             "%(field_type)s."), ["value", "field", "field_type"])
PLP1011 = Error("PLP1011", _("Invalid task state passed to purge: %(state)s."), ["state"])
PLP1012 = Error("PLP1012", _("No task state given to parameters list for delete."), [])
PLP1013 = Error("PLP1013", _("Checksum does not match calculated value."), [])
PLP1014 = Error("PLP1014", _("The configuration value for the key '%(key)s' in "
                             "section '%(section)s' is not valid for the following "
                             "reason: %(reason)s"), ["key", "section", "reason"])
PLP1015 = Error("PLP1015", _("The JSON data must be of type '%(data_type)s'."),
                ['data_type'])
