"""
Steps:

1) Retrieve patient information based on variants
2) Traverse Patient and organize them via HPO terms
3) Build Clustering of HPO terms



# Interesting packages:

https://pyhpo.readthedocs.io/en/latest/
https://pheatmap.readthedocs.io/en/stable/BasicUsage.html

# Interesting papers:

Shu, B. et al. (2022). 
Human phenotype ontology annotation and cluster analysis for pulmonary atresia to unravel clinical outcomes. 
Frontiers in Cardiovascular Medicine, 9, 898289. https://doi.org/10.3389/fcvm.2022.898289

Westbury, S. K. et al. BRIDGE-BPD Consortium. (2015). Human phenotype ontology annotation and cluster analysis #
to unravel genetic defects in 707 cases with unexplained bleeding and platelet disorders. 
Genome Medicine, 7(1), 36. https://doi.org/10.1186/s13073-015-0151-5

"""


import argparse
import datetime
import requests
import simplejson
import pprint


class FHIRRetriever:
    def __init__(self, fhir_auth_cookie, kids_first_fhir_url="https://kf-api-fhir-service.kidsfirstdrc.org/"):
        self.fhir_auth_cookie = fhir_auth_cookie
        self.KIDS_FIRST_FHIR= kids_first_fhir_url

    def retrieve_hpo_terms(self, patients):
        """Retrieve the hpo terms for each patients, returning a dictionary with key the Patient Identifier and
        the value the list of HPO terms found"""
        #https://kf-api-fhir-service.kidsfirstdrc.org/Condition?patient.identifier=PT_8NNFJYG5&_format=json
        
        # patient_id = "PT_8NNFJYG5"
        for patient_id in patients:
            target_url = f"{self.KIDS_FIRST_FHIR}/Condition?patient.identifier={patient_id}&format=json"
            req = requests.get(target_url)
            try:
                req_j = req.json()
                for entry in req_j['entry']:
                    for entry in entries:
                        code = entry['resource']['code']
                        pprint.pprint(code)
                        print("-"*40 + "\n")
            except KeyError:
                print ("Unable to serialize to JSON")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve HPO terms from the Kids First FHIR Server')
    parser.add_argument("--include_fhir_authentication_cookie", required=True, 
                        help="The Authorization cookie from the INCLUDE FHIR Server (https://kf-api-fhir-service.kidsfirstdrc.org/) \
                            To obtain the cookie, open the Chorme or Firefox console, go to the Application tab and copy the value \
                            contained in `AWSELBAuthSessionCookie-0`.")
    args = parser.parse_args()
    fhir_retriever = FHIRRetriever(args.include_fhir_authentication_cookie)
    req = fhir_retriever.retrieve_hpo_terms(["PT_8NNFJYG5"])

