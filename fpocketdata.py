import os
import pandas as pd 

#Stores for key features
pocket_numbers = []
druggability_scores = []
volume = []
hydrophobicity_scores = []
alpha_sphere_densities = []
polarity_scores = []

#File path to be adjusted as needed
file_path = os.path.expanduser("path/to/info.txt")
# for example, file_path = os.path.expanduser("~/Desktop/ghr_cat_model_2_out/ghr_cat_model_2_info.txt")


#Read the file
with open(file_path, "r") as file:
    lines = file.readlines()
    
    for i in range(len(lines)):
        line = lines[i].strip()
        
        if line.startswith("Pocket"):
            pocket_numbers.append(int(line.split()[1].strip(':')))
        elif "Druggability Score" in line:
            druggability_scores.append(float(line.split(':')[-1].strip()))
        elif "Volume" in line:
            volume.append(float(line.split(':')[-1].strip()))    
        elif "Hydrophobicity score" in line:
            hydrophobicity_scores.append(float(line.split(':')[-1].strip()))
        elif "Alpha sphere density" in line:
            alpha_sphere_densities.append(float(line.split(':')[-1].strip()))
        elif "Polarity score" in line:
            polarity_scores.append(float(line.split(':')[-1].strip()))    
            

# Ensure all lists are the same length by filling missing values
max_length = max(len(pocket_numbers), len(druggability_scores), len(volume),
                 len(hydrophobicity_scores), len(alpha_sphere_densities), len(polarity_scores))

def pad_list(lst, length):
    while len(lst) < length:
        lst.append(None)  # Use None to indicate missing values

pad_list(pocket_numbers, max_length)
pad_list(druggability_scores, max_length)
pad_list(volume, max_length)
pad_list(hydrophobicity_scores, max_length)
pad_list(alpha_sphere_densities, max_length)
pad_list(polarity_scores, max_length)


#Dataframe with pocket number and key features                    
df = pd.DataFrame({
    "Pocket Number": pocket_numbers,
    "Druggability Score": druggability_scores,
    "Volume": volume,
    "Hydrophobicity Score": hydrophobicity_scores,
    "Alpha Sphere Density": alpha_sphere_densities,
    "Polarity Score": polarity_scores
})            

#print(df)

#filtering out pockets with low druggability scores
#used druggability score greater than 0.5 (per Michel et al and Cunha et al)
#Michel M, Visnes T, Homan EJ, Seashore-Ludlow B, Hedenström M, Wiita E, Vallin K, Paulin CBJ, Zhang J, Wallner O, Scobie M, Schmidt A, Jenmalm-Jensen A, Warpman Berglund U, Helleday T. Computational and Experimental Druggability Assessment of Human DNA Glycosylases. ACS Omega. 2019 Jul 5;4(7):11642-11656. doi: 10.1021/acsomega.9b00162. PMID: 31460271; PMCID: PMC6682003.
#Cunha AES, Loureiro RJS, Simões CJV, Brito RMM. Unveiling New Druggable Pockets in Influenza Non-Structural Protein 1: NS1–Host Interactions as Antiviral Targets for Flu. International Journal of Molecular Sciences. 2023; 24(3):2977. https://doi.org/10.3390/ijms24032977

df_filtered = df[df["Druggability Score"] > 0.5].copy()

#print(df_filtered)

#creating ranking system with highest priority placed on druggability score
#weight numbers are arbitrary numbers assigned
df_filtered.loc[:, "Ranking Score"] = (
    df_filtered["Druggability Score"] * 0.5 + #50% importance to druggability
    df_filtered["Hydrophobicity Score"] * 0.3 + #30% importance
    df_filtered["Alpha Sphere Density"] * 0.2  #20% importance
)

#Sort
df_filtered = df_filtered.sort_values(by= "Ranking Score", ascending= False)

#Find and print best pocket
best_pocket = df_filtered.iloc[0]

best_pocket_number = int(best_pocket["Pocket Number"])

# Retrieve original data for best pocket
with open(file_path, "r") as file:
    lines = file.readlines()
    extract = False
    best_pocket_data = []
    for line in lines:
        if line.startswith(f"Pocket {best_pocket_number} :"):
            extract = True
        elif extract and line.startswith("Pocket") and not line.startswith(f"Pocket {best_pocket_number} :"):
            break
        if extract:
            best_pocket_data.append(line.strip())

# Print best pocket with original data from txt file
print("Best Pocket Candidate:")
print("\n".join(best_pocket_data))






#print("Best Pocket Candidate: ")
#print(best_pocket)

