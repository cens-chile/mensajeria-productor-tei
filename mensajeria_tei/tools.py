from enum import Enum

from fhirclient.models.bundle import BundleEntry


class ProfileList(Enum):
    iniciar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleIniciarLE"
    referenciar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleReferenciarLE"
    revisar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleRevisarLE"
    priorizar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundlePriorizarLE"
    agendar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleAgendarLE"
    atender = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleAtenderLE"
    terminar = "https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/BundleTerminarLE"



def find_resource_in_bundle(bundle, reference):
    if 'entry' not in bundle.as_json() or len(bundle.entry) == 0:
        return None
    for entry in bundle.entry:
        bundle_entry = BundleEntry(jsondict=entry.as_json())
        if 'fullUrl' in bundle_entry.as_json() and bundle_entry.fullUrl.endswith(reference):
            return bundle_entry.resource
    return None

def find_resource_in_bundle_by_profile(bundle, profile):
    if 'entry' not in bundle.as_json() or len(bundle.entry) == 0:
        return None
    for entry in bundle.entry:
        bundle_entry = BundleEntry(jsondict=entry.as_json())
        if 'resource' not in bundle_entry.as_json():
            return None
        if 'meta' not in bundle_entry.resource.as_json():
            return None
        if 'profile' not in bundle_entry.resource.meta.as_json():
            return None
        profile_list = bundle_entry.resource.meta.profile
        if profile in profile_list:
            return bundle_entry.resource
    return None