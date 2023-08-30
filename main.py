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
    def __init__(self, kids_first_fhir_url="https://kf-api-fhir-service.kidsfirstdrc.org/"):
        #self.fhir_auth_cookie = fhir_auth_cookie
        self.KIDS_FIRST_FHIR= kids_first_fhir_url

    def retrieve_hpo_terms(self, patients):
        """Retrieve the hpo terms for each patients, returning a dictionary with key the Patient Identifier and
        the value the list of HPO terms found"""
        #https://kf-api-fhir-service.kidsfirstdrc.org/Condition?patient.identifier=PT_8NNFJYG5&_format=json
        
        # patient_id = "PT_8NNFJYG5"
        patients_codes =[]
        for patient_id in patients:
            target_url = f"{self.KIDS_FIRST_FHIR}Condition?subject.identifier={patient_id}&_tag=SD_65064P2Z&_format=json"
            print(f"Target url {target_url}")
            req = requests.get(target_url)
            try:
                req_j = req.json()
                
                codes = []
                for entry in req_j['entry']:
                    code_entry = entry['resource']['code']
                    pprint.pprint(code_entry)
                    print("-"*40 + "\n")
                    for item in code_entry['coding']:
                        codes.append(item['code'])
                patients_codes.append({patient_id : codes})
            except KeyError:
                print ("Unable to serialize to JSON")
        print(patients_codes)
        return patients_codes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve HPO terms from the Kids First FHIR Server')
    # parser.add_argument("--include_fhir_authentication_cookie", required=True, 
    #                     help="The Authorization cookie from the INCLUDE FHIR Server (https://kf-api-fhir-service.kidsfirstdrc.org/) \
    #                         To obtain the cookie, open the Chorme or Firefox console, go to the Application tab and copy the value \
    #                         contained in `AWSELBAuthSessionCookie-0`.")
    args = parser.parse_args()
    fhir_retriever = FHIRRetriever()
    req = fhir_retriever.retrieve_hpo_terms(["PT_02CP8NYR", "PT_02ZWYB9A", "PT_8NNFJYG5"])

