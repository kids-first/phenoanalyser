"""
Steps:

1) Retrieve patient information based on variants
2) Traverse Patient and organize them via HPO, NCIT and MONDO terms
3) Build Clustering of HPO terms



# Interesting packages:

https://pyhpo.readthedocs.io/en/latest/
https://pheatmap.readthedocs.io/en/stable/BasicUsage.html

# Interesting papers:

Shu, B. et al. (2022). 
Human phenotype ontology annotation and cluster analysis for pulmonary atresia to unravel clinical outcomes. 
Frontiers in Cardiovascular Medicine, 9, 898289. https://doi.org/10.3389/fcvm.2022.898289

--> Bottom two plots of figure 2 is what to replicate

Westbury, S. K. et al. BRIDGE-BPD Consortium. (2015). Human phenotype ontology annotation and cluster analysis #
to unravel genetic defects in 707 cases with unexplained bleeding and platelet disorders. 
Genome Medicine, 7(1), 36. https://doi.org/10.1186/s13073-015-0151-5

"""


import argparse
import datetime
import requests
import simplejson
import pprint
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt


class FHIRRetriever:
    def __init__(self, kids_first_fhir_url="https://kf-api-fhir-service.kidsfirstdrc.org/"):
        #self.fhir_auth_cookie = fhir_auth_cookie
        self.KIDS_FIRST_FHIR= kids_first_fhir_url

    def retrieve_all_terms(self, df_patients):
        """Retrieve the hpo terms for each patients, returning a dictionary with key the Patient Identifier and
        the value the list of HPO terms found"""
        #https://kf-api-fhir-service.kidsfirstdrc.org/Condition?patient.identifier=PT_8NNFJYG5&_format=json
        
        
        #patients_codes =[]
        patients_codes_dict ={}
        for index, row in df.iterrows():
            target_url = f"{self.KIDS_FIRST_FHIR}Condition?subject.identifier={row['participant_id']}&_format=json"
            #print(f"Target url {target_url}")
            req = requests.get(target_url)
            try:
                req_j = req.json()
                
                codes = []
                for entry in req_j['entry']:
                    code_entry = entry['resource']['code']
                    #pprint.pprint(code_entry)
                    #print("-"*40 + "\n")
                    for item in code_entry['coding']:
                        codes.append(item['code'])
                #patients_codes.append({row['participant_id'] : codes})
                patients_codes_dict[row['participant_id']] = codes
            except KeyError:
                print ("Unable to serialize to JSON for ", target_url)
        #pprint.pprint(patients_codes)
        #pprint.pprint(patients_codes_dict)
        #print ("\n")
        #print(type(patients_codes))
        #print(type(patients_codes_dict))
        #print ("\n")

        return patients_codes_dict



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve HPO terms from the Kids First FHIR Server')
    # parser.add_argument("--include_fhir_authentication_cookie", required=True, 
    #                     help="The Authorization cookie from the INCLUDE FHIR Server (https://kf-api-fhir-service.kidsfirstdrc.org/) \
    #                         To obtain the cookie, open the Chrome or Firefox console, go to the Application tab and copy the value \
    #                         contained in `AWSELBAuthSessionCookie-0`.")
    parser.add_argument("patient_list", help="CSV with patient list and dataset tag")
    args = parser.parse_args()
    fhir_retriever = FHIRRetriever()
    
    df = pd.read_csv(args.patient_list, sep="\t")
    patients_codes_dict = fhir_retriever.retrieve_all_terms(df)
    
    codes_seq = ()
    for patient in patients_codes_dict:
        codes_seq = codes_seq + tuple(patients_codes_dict[patient])

    print ("\n")
    print ('codes_seq', codes_seq)

    counts = Counter(codes_seq)
    dfplot = pd.DataFrame.from_dict(counts, orient='index')
    dfplot.plot(kind='bar')

    plt.title('Frequency of all terms')
    plt.xlabel('Count')
    plt.ylabel('Terms')
    #displaying to allow for manual fine tuning of plot features
    plt.show()
    plt.savefig("Frequency_of_all_terms.png")

    #separating out NCIT, MONDO and HPO terms
    hpo_codes_seq = ()
    mondo_codes_seq = ()
    ncit_codes_seq = ()
    for patient in patients_codes_dict:
        patient_all_codes_seq = ()
        patient_all_codes_seq = tuple(patients_codes_dict[patient])

        for terms_tup in patient_all_codes_seq:


            if terms_tup.startswith('H'):
                hpo_codes_seq = hpo_codes_seq + (terms_tup,)
            
            if terms_tup.startswith('M'):
                mondo_codes_seq = mondo_codes_seq + (terms_tup,)
            
            if terms_tup.startswith('N'):
                ncit_codes_seq = ncit_codes_seq + (terms_tup,)

    print ("\n\n\n")
    print ('hpo_codes_seq', hpo_codes_seq)
    counts = Counter(hpo_codes_seq)
    dfplot = pd.DataFrame.from_dict(counts, orient='index')
    dfplot.plot(kind='bar')

    plt.title('Frequency of HPO terms')
    plt.xlabel('Count')
    plt.ylabel('Terms')
    #displaying to allow for manual fine tuning of plot features
    plt.show()
    plt.savefig("Frequency_of_HPO_terms.png")

    print ("\n\n\n")
    print ('mondo_codes_seq', mondo_codes_seq)
    counts = Counter(mondo_codes_seq)
    dfplot = pd.DataFrame.from_dict(counts, orient='index')
    dfplot.plot(kind='bar')

    plt.title('Frequency of MONDO terms')
    plt.xlabel('Count')
    plt.ylabel('Terms')
    #displaying to allow for manual fine tuning of plot features
    plt.show()
    plt.savefig("Frequency_of_MONDO_terms.png")

    
    print ("\n\n\n")
    print ('ncit_codes_seq', ncit_codes_seq)
    counts = Counter(ncit_codes_seq)
    dfplot = pd.DataFrame.from_dict(counts, orient='index')
    dfplot.plot(kind='bar')

    plt.title('Frequency of NCIT terms')
    plt.xlabel('Count')
    plt.ylabel('Terms')
    #displaying to allow for manual fine tuning of plot features
    plt.show()
    plt.savefig("Frequency_of_NCIT_terms.png")


