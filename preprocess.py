import pandas as pd
import os

# Get movie path
CWD = os.getcwd()
movies_path = os.path.join(CWD, "dataset", "IMDb movies.csv")
output_path = os.path.join(CWD, "dataset", "IMDb movies preprocessed.csv")

# Get movies dataset
movies = pd.read_csv(os.path.join(CWD, "dataset", "IMDb movies.csv"))
# Remove nan
movies = movies.where(pd.notnull(movies), "")


#imdb_title_id,title,original_title,year,date_published,genre,duration,country,language,director,writer,production_company,actors,description,avg_vote,votes,budget,usa_gross_income,worlwide_gross_income,metascore,reviews_from_users,reviews_from_critics

movies["description"] = "the title is " + movies["title"] + \
                            ", original title is " + movies["original_title"] + \
                                    ", genre is " + movies["genre"] + \
                                        ", director is " + movies["director"] + \
                                            ", actors are " + movies["actors"] + \
                                                ", movie plot is " + movies["description"]

movies = movies[["imdb_title_id", "description"]]

print(movies)

movies.to_csv(output_path, index=False)
                            