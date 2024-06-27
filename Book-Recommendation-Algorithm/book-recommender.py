# Books Recommendation System

import re
import operator
import numpy as np
import pandas as pd
from collections import Counter
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from thefuzz import process
import sys
import json


import warnings

warnings.filterwarnings("ignore")
# Dataset

# def get_closest_match_with_author(book_name_search, book_author_search, book_list):
#     search_query = f"{book_name_search} by {book_author_search}"
#     highest = process.extractOne(search_query, book_list)
#     return highest[0]


def get_book_details_by_isbn_and_name(book_isbn, book_name, book_details):
    for isbn, title, author in book_details:
        if isbn == book_isbn and title.lower() == book_name.lower():
            return isbn, title, author  # Direct match found by ISBN and name confirmed

    # If no direct match is found by ISBN or the book name does not match
    return None, None, None


# books = pd.read_csv(r"./Datasets/Books.csv", delimiter=';', error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
books = pd.read_csv(
    r"./Datasets/Books.csv",
    delimiter=";",
    encoding="ISO-8859-1",
)
# ratings = pd.read_csv(r"./Datasets/Ratings.csv", delimiter=';', error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
ratings = pd.read_csv(
    r"./Datasets/Ratings.csv",
    delimiter=";",
    encoding="ISO-8859-1",
)
# users = pd.read_csv(r"./Datasets/Users.csv", delimiter=';', error_bad_lines=False, encoding='ISO-8859-1', warn_bad_lines=False)
users = pd.read_csv(
    r"./Datasets/Users.csv",
    delimiter=";",
    encoding="ISO-8859-1",
)

# Pre-processing
# Books Dataset Pre-processing

books.head()

# books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)
books.head()

books.isnull().sum()

# books.loc[books['Author'].isnull(),:]
books.loc[books["Author"].isnull(), :]

books.loc[books["Publisher"].isnull(), :]

# books.at[187689 ,'Author'] = 'Other'
books.at[187689, "Author"] = "Other"

books.at[128890, "Publisher"] = "Other"
books.at[129037, "Publisher"] = "Other"

books["Year"].unique()

pd.set_option("display.max_colwidth", +1)

books.loc[books["Year"] == "DK Publishing Inc", :]

books.loc[books["Year"] == "Gallimard", :]

books.at[209538, "Publisher"] = "DK Publishing Inc"
books.at[209538, "Year"] = 2000
books.at[209538, "Title"] = (
    "DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)"
)
books.at[209538, "Author"] = "Michael Teitelbaum"

books.at[221678, "Publisher"] = "DK Publishing Inc"
books.at[221678, "Year"] = 2000
books.at[209538, "Title"] = (
    "DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)"
)
books.at[209538, "Author"] = "James Buckley"

books.at[220731, "Publisher"] = "Gallimard"
books.at[220731, "Year"] = "2003"
books.at[209538, "Title"] = "Peuple du ciel - Suivi de Les bergers "
books.at[209538, "Author"] = "Jean-Marie Gustave Le ClÃ?Â©zio"

books["Year"] = books["Year"].astype(int)

count = Counter(books["Year"])
[k for k, v in count.items() if v == max(count.values())]

# books.loc[books['Year'] > 2021, 'Year'] = 2002
books.loc[books["Year"] == 0, "Year"] = 2002

books["ISBN"] = books["ISBN"].str.upper()

books.drop_duplicates(keep="last", inplace=True)
books.reset_index(drop=True, inplace=True)

# books.info()

books.head()
# Users Dataset Pre-processing

users.head()

required = users[users["Age"] <= 80]
required = required[required["Age"] >= 10]

mean = round(required["Age"].mean())
mean

# outliers with age grater than 80 are substituted with mean
users.loc[users["Age"] > 80, "Age"] = mean
# outliers with age less than 10 years are substitued with mean
users.loc[users["Age"] < 10, "Age"] = mean
users["Age"] = users["Age"].fillna(mean)  # filling null values with mean
users["Age"] = users["Age"].astype(int)  # changing Datatype to int

list_ = users.Location.str.split(", ")

city = []
state = []
country = []
count_no_state = 0
count_no_country = 0

for i in range(0, len(list_)):
    # removing invalid entries too
    if (
        list_[i][0] == " "
        or list_[i][0] == ""
        or list_[i][0] == "n/a"
        or list_[i][0] == ","
    ):
        city.append("other")
    else:
        city.append(list_[i][0].lower())

    if len(list_[i]) < 2:
        state.append("other")
        country.append("other")
        count_no_state += 1
        count_no_country += 1
    else:
        # removing invalid entries
        if (
            list_[i][1] == " "
            or list_[i][1] == ""
            or list_[i][1] == "n/a"
            or list_[i][1] == ","
        ):
            state.append("other")
            count_no_state += 1
        else:
            state.append(list_[i][1].lower())

        if len(list_[i]) < 3:
            country.append("other")
            count_no_country += 1
        else:
            if (
                list_[i][2] == ""
                or list_[i][1] == ","
                or list_[i][2] == " "
                or list_[i][2] == "n/a"
            ):
                country.append("other")
                count_no_country += 1
            else:
                country.append(list_[i][2].lower())

users = users.drop("Location", axis=1)

temp = []
for ent in city:
    # handling cases where city/state entries from city list as state is already given
    c = ent.split("/")
    temp.append(c[0])

df_city = pd.DataFrame(temp, columns=["City"])
df_state = pd.DataFrame(state, columns=["State"])
df_country = pd.DataFrame(country, columns=["Country"])

users = pd.concat([users, df_city], axis=1)
users = pd.concat([users, df_state], axis=1)
users = pd.concat([users, df_country], axis=1)

users.drop_duplicates(keep="last", inplace=True)
users.reset_index(drop=True, inplace=True)

# users.info()

users.head()
# Books-Ratings Dataset Pre-processing

ratings.head()

ratings.isnull().sum()

flag = 0
k = []
reg = "[^A-Za-z0-9]"

for x in ratings["ISBN"]:
    z = re.search(reg, x)
    if z:
        flag = 1

# if flag == 1:
#     print("False")
# else:
#     print("True")

bookISBN = books["ISBN"].tolist()
reg = "[^A-Za-z0-9]"
for index, row_Value in ratings.iterrows():
    z = re.search(reg, row_Value["ISBN"])
    if z:
        f = re.sub(reg, "", row_Value["ISBN"])
        if f in bookISBN:
            ratings.at[index, "ISBN"] = f

ratings["ISBN"] = ratings["ISBN"].str.upper()

ratings.drop_duplicates(keep="last", inplace=True)
ratings.reset_index(drop=True, inplace=True)

# ratings.info()

ratings.head()
# <h3><b>Merging of all three Tables
# Merging Books, Users and Rating Tables in One

dataset = pd.merge(books, ratings, on="ISBN", how="inner")
dataset = pd.merge(dataset, users, on="User-ID", how="inner")
# dataset.info()
# Divide complete data on the basis of Implicit and Explicit ratings datasets

dataset1 = dataset[dataset["Rating"] != 0]
dataset1 = dataset1.reset_index(drop=True)
dataset1.shape

dataset2 = dataset[dataset["Rating"] == 0]
dataset2 = dataset2.reset_index(drop=True)
dataset2.shape

dataset1.head()

# bookName = input("Enter the name of the book: ")
# bokISBN = input("Enter the ISBN of the book: ")
# number = int(input("Enter number of books to recommend: "))

bokISBN = sys.argv[1]
bookName = sys.argv[2]
number = int(sys.argv[3])

book_details = [
    (row["ISBN"], row["Title"], row["Author"]) for index, row in books.iterrows()
]

isbn, title, author = get_book_details_by_isbn_and_name(
    bookISBN, bookName, book_details
)


# <h5><b> 1. Popularity Based (Top In whole collection)


def popularity_based(dataframe, n):
    if n >= 1 and n <= len(dataframe):
        data = (
            pd.DataFrame(dataframe.groupby("ISBN")["Rating"].count())
            .sort_values("Rating", ascending=False)
            .head(n)
        )
        result = pd.merge(
            data,
            books,
            on="ISBN",
        )
        return result
    return "Invalid number of books entered!!"


popularity_based(dataset1, number)
# <h5><b>2. Popularity Based (Top In a given place)


def search_unique_places(dataframe, place):
    place = place.lower()

    if place in list(dataframe["City"].unique()):
        return dataframe[dataframe["City"] == place]
    elif place in list(dataframe["State"].unique()):
        return dataframe[dataframe["State"] == place]
    elif place in list(dataframe["Country"].unique()):
        return dataframe[dataframe["Country"] == place]
    else:
        return "Invalid Entry"


# place = input("Enter the name of place: ")
place = sys.argv[4]
data = search_unique_places(dataset1, place)

if isinstance(data, pd.DataFrame):
    data = popularity_based(data, number)

data
# 3. Books by same author, publisher of given book name

print("[")


def print_json_output(data, category):
    output = json.dumps(
        {f"Recommended Books {category}": data}, ensure_ascii=False, indent=4
    )
    print(output)


def get_books(dataframe, name, n):
    data = dataset1[dataset1["Title"] != name]

    # Books by the same author
    author_books = []
    author = dataframe["Author"].iloc[0]
    if author in data["Author"].unique():
        books_by_author = (
            data[data["Author"] == author]
            .sort_values(by=["Rating"], ascending=False)
            .head(n)
        )
        for _, book in books_by_author.iterrows():
            author_books.append(
                {
                    "ISBN": book["ISBN"],
                    "Title": book["Title"],
                    "Author": book["Author"],
                    "Year": int(book["Year"]),
                    "Publisher": book["Publisher"],
                }
            )
    print_json_output(author_books, "1. By Same Author")
    print(",")
    # Books by the same publisher
    publisher_books = []
    publisher = dataframe["Publisher"].iloc[0]
    if publisher in data["Publisher"].unique():
        books_by_publisher = (
            data[data["Publisher"] == publisher]
            .sort_values(by=["Rating"], ascending=False)
            .head(n)
        )
        for _, book in books_by_publisher.iterrows():
            publisher_books.append(
                {
                    "ISBN": book["ISBN"],
                    "Title": book["Title"],
                    "Author": book["Author"],
                    "Year": int(book["Year"]),
                    "Publisher": book["Publisher"],
                }
            )
    print_json_output(publisher_books, "2. By Same Publisher")
    print(",")


if bookName in dataset1["Title"].unique():
    d = dataset1[dataset1["Title"] == bookName]
    get_books(d, bookName, number)
# else:
#     print("Invalid Book Name!!")

# if bookName in list(dataset1['Title'].unique()):
#     d = dataset1[dataset1['Title'] == bookName]
#     get_books(d, bookName, number)
# else:
#     # print(bookName)
#     print("Invalid Book Name!!")
# <h5><b>4. Books popular Yearly

data = pd.DataFrame(dataset1.groupby("ISBN")["Rating"].count()).sort_values(
    "Rating", ascending=False
)
data = pd.merge(data, books, on="ISBN")

years = set()
indices = []
for ind, row in data.iterrows():
    if row["Year"] in years:
        indices.append(ind)
    else:
        years.add(row["Year"])

data = data.drop(indices)
data = data.drop("Rating", axis=1)
data = data.sort_values("Year")

pd.set_option("display.max_rows", None, "display.max_columns", None)
data
# 5. Average Weighted Ratings


def avgRating(newdf, df):
    newdf["Average Rating"] = 0
    for x in range(len(newdf)):
        l = list(df.loc[df["Title"] == newdf["Title"][x]]["Rating"])
        newdf["Average Rating"][x] = sum(l) / len(l)
    return newdf


df = pd.DataFrame(dataset1["Title"].value_counts())
df.reset_index(inplace=True)
df.columns = ["Title", "Total-Ratings"]

df["Total-Ratings"] = df["Title"]
df["Title"] = df.index
df.reset_index(level=0, inplace=True)
df = df.drop("index", axis=1)

# df = avgRating(df, dataset1)
# df.to_pickle('weightedData')
df = pd.read_pickle("weightedData")

C = df["Average Rating"].mean()

m = df["Total-Ratings"].quantile(0.90)


def weighted_rating(x, m=m, C=C):
    v = x["Total-Ratings"]  # v - number of votes
    R = x["Average Rating"]  # R - Average Rating
    return (v / (v + m) * R) + (m / (m + v) * C)


df = df.loc[df["Total-Ratings"] >= m]

df["score"] = df.apply(weighted_rating, axis=1)
df = df.sort_values("score", ascending=False)

# print("\nRecommended Books 1. Average Weighted Ratings:\n")
df.head(number)
# 6. Collaborative Filtering (User-Item Filtering)
# Selecting books with total ratings equals to or more than 50 (Because of availability of limited resources)

df = pd.DataFrame(dataset1["Title"].value_counts())
df.columns = ["Total-Ratings"]
df["Title"] = df.index
df.reset_index(drop=True, inplace=True)

df = dataset1.merge(df, on="Title", how="left")
df = df.drop(["Age", "City", "State", "Country"], axis=1)

# Filter for popular books based on a threshold
popularity_threshold = 20
popular_book = df[df["Total-Ratings"] >= popularity_threshold]
popular_book.reset_index(drop=True, inplace=True)

testdf = pd.DataFrame()
testdf["ISBN"] = popular_book["ISBN"]
testdf["Rating"] = popular_book["Rating"]
testdf["User-ID"] = popular_book["User-ID"]
testdf = testdf[["User-ID", "Rating"]].groupby(testdf["ISBN"])

listOfDictonaries = []
indexMap = {}
reverseIndexMap = {}
ptr = 0

for groupKey in testdf.groups.keys():
    tempDict = {}
    groupDF = testdf.get_group(groupKey)
    for i in range(0, len(groupDF)):
        tempDict[groupDF.iloc[i, 0]] = groupDF.iloc[i, 1]
    indexMap[ptr] = groupKey
    reverseIndexMap[groupKey] = ptr
    ptr = ptr + 1
    listOfDictonaries.append(tempDict)

dictVectorizer = DictVectorizer(sparse=True)
vector = dictVectorizer.fit_transform(listOfDictonaries)
pairwiseSimilarity = cosine_similarity(vector)


# def printBookDetails(bookID):
#     print(dataset1[dataset1['ISBN'] == bookID]['Title'].values[0])


def getTopRecommandations(bookID):
    if bookID not in reverseIndexMap:
        # print(f"Error: BookID {bookID} not found.")
        return []

    collaborative = []
    row = reverseIndexMap[bookID]

    mn = 0
    similar = []
    for i in np.argsort(pairwiseSimilarity[row])[:-2][::-1]:
        current_book_id = indexMap[i]
        current_book = dataset1[dataset1["ISBN"] == current_book_id]
        if not current_book.empty:
            current_book_details = current_book.iloc[0]
            if current_book_details["Title"] not in similar:
                if mn >= number:
                    break
                mn += 1
                book_info = {
                    "ISBN": str(current_book_details["ISBN"]),
                    "Title": current_book_details["Title"],
                    "Author": current_book_details.get("Author", "N/A"),
                    "Year": int(current_book_details["Year"]),
                    # Assuming 'Publisher' might not be present
                    "Publisher": current_book_details.get("Publisher", "N/A"),
                }
                similar.append(current_book_details["Title"])
                # printBookDetails(current_book_id)
                collaborative.append(book_info)
    return collaborative


k = list(dataset1["Title"])
m = list(dataset1["ISBN"])

collaborative = getTopRecommandations(m[k.index(bookName)])

# Prepare JSON output with the top recommended books including details
output = json.dumps(
    {"Recommended Books 3. Collaborative": collaborative}, ensure_ascii=False, indent=4
)
print(output)
print(",")

# 7. Correlation Based

popularity_threshold = 20

user_count = dataset1["User-ID"].value_counts()
data = dataset1[
    dataset1["User-ID"].isin(user_count[user_count >= popularity_threshold].index)
]
rat_count = data["Rating"].value_counts()
data = data[data["Rating"].isin(rat_count[rat_count >= popularity_threshold].index)]

matrix = data.pivot_table(index="User-ID", columns="ISBN", values="Rating").fillna(0)

average_rating = pd.DataFrame(dataset1.groupby("ISBN")["Rating"].mean())
average_rating["ratingCount"] = pd.DataFrame(ratings.groupby("ISBN")["Rating"].count())
average_rating.sort_values("ratingCount", ascending=False).head()

isbn = books.loc[books["Title"] == bookName].reset_index(drop=True).iloc[0]["ISBN"]
row = matrix[isbn]
correlation = pd.DataFrame(matrix.corrwith(row), columns=["Pearson Corr"])
corr = correlation.join(average_rating["ratingCount"])

res = corr.sort_values("Pearson Corr", ascending=False).head(number + 1)[1:].index
# print("\nRecommended Books 2. Correlation Based: \n")
# print(corr_books)
corr_books = pd.merge(pd.DataFrame(res, columns=["ISBN"]), books, on="ISBN")
corr_books_json = corr_books.to_json(orient="records", force_ascii=False)

# Print JSON
print(
    json.dumps(
        {"Recommended Books 4. Correlation Based": json.loads(corr_books_json)},
        ensure_ascii=False,
        indent=4,
    )
)
print(",")

# <h5><b>8. Nearest Neighbours Based

data = (
    dataset1.groupby(by=["Title"])["Rating"]
    .count()
    .reset_index()
    .rename(columns={"Rating": "Total-Rating"})[["Title", "Total-Rating"]]
)

data["Title"] = data["Title"].astype(str)
dataset1["Title"] = dataset1["Title"].astype(str)

result = pd.merge(data, dataset1, on="Title")


result = result[result["Total-Rating"] >= popularity_threshold]
result = result.reset_index(drop=True)

matrix = (
    result.set_index("Title")
    .pivot_table(index="Title", columns="User-ID", values="Rating")
    .fillna(0)
)

up_matrix = csr_matrix(matrix)

model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(up_matrix)

distances, indices = model.kneighbors(
    matrix.loc[bookName].values.reshape(1, -1), n_neighbors=number + 1
)

recommended_books = []
titles_seen = set()  # Set to track seen titles

# Skip the first one if it is the query book itself
for i in range(1, len(distances.flatten())):
    index = indices.flatten()[i]
    book_info = result.iloc[index]
    if book_info["Title"] not in titles_seen:  # Check if the title is already processed
        titles_seen.add(book_info["Title"])  # Add title to the set
        recommended_books.append(
            {
                # Convert to string if ISBN is numeric
                "ISBN": str(book_info["ISBN"]),
                "Title": book_info["Title"],
                "Author": book_info["Author"],
                # Ensure year is a native Python int
                "Year": int(book_info["Year"]),
                "Publisher": book_info["Publisher"],
            }
        )
    # else:
    #     print(
    #         f"Duplicate title '{book_info['Title']}' with different ISBN not added.")

# Output as JSON
output = json.dumps(
    {"Recommended Books 5. Nearest Neighbours Based": recommended_books},
    ensure_ascii=False,
    indent=4,
)

print(output)
print(",")

# <h5><b>9. Content Based

popularity_threshold = 20
popular_book = df[df["Total-Ratings"] >= popularity_threshold]
popular_book = popular_book.reset_index(drop=True)
popular_book.shape

# Transform book titles into TF-IDF features
tf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
tfidf_matrix = tf.fit_transform(popular_book["Title"])
tfidf_matrix.shape

normalized_df = tfidf_matrix.astype(np.float32)
cosine_similarities = cosine_similarity(normalized_df, normalized_df)
cosine_similarities.shape

# Calculate cosine similarities between books
# cosine_similarities = cosine_similarity(normalized_df)

# Find the index of the book being queried
isbn = books.loc[books["Title"] == bookName].reset_index(drop=True).iloc[0]["ISBN"]

# print("isbn", isbn)

content = []

idx = popular_book.index[popular_book["ISBN"] == isbn].tolist()[0]

# Get the most similar books based on cosine similarity
similar_indices = cosine_similarities[idx].argsort()[::-1]
content_details = []
titles_seen = set()  # Set to track seen titles and prevent duplicates

for i in similar_indices:
    current_title = popular_book.at[i, "Title"]
    if current_title != bookName and len(content_details) < number:
        if current_title not in titles_seen:  # Check if the title is already processed
            book_details = {
                "ISBN": popular_book.at[i, "ISBN"],
                "Title": current_title,
                "Author": popular_book.at[i, "Author"],
                "Year": int(popular_book.at[i, "Year"]),
                "Publisher": popular_book.at[i, "Publisher"],
            }
            content_details.append(book_details)
            titles_seen.add(current_title)  # Add title to the set
        # else:
        #     print(
        #         f"Duplicate title '{current_title}' with different ISBN not added.")

        # Prepare JSON output with the recommended book details
output = json.dumps(
    {"Recommended Books 6. Content Based": content_details},
    ensure_ascii=False,
    indent=4,
)

print(output)
print(",")


# 10. Hybrid Approach (Content+Collaborative) Using percentile

k = float(1 / number)
z = [1 - k * x for x in range(number)]

dictISBN = {}
for index, book in enumerate(collaborative):
    isbn = book["ISBN"]
    dictISBN[isbn] = z[index]

for index, book in enumerate(content):
    isbn = book["ISBN"]
    if isbn not in dictISBN:
        dictISBN[isbn] = z[index]
    else:
        dictISBN[isbn] += z[index]

# Sort the ISBNs by their calculated weights in descending order
sorted_ISBNs = dict(sorted(dictISBN.items(), key=operator.itemgetter(1), reverse=True))

recommended_ISBNs = []
book_details_list = []
titles_seen = set()  # To track titles and avoid duplicates
count = 0
# print("Input Book:\n")
# print(bookName)
# print("\nRecommended Books:\n")
for isbn, weight in sorted_ISBNs.items():
    if count >= number:
        break
    book_details = books.loc[books["ISBN"] == isbn].reset_index(drop=True)
    if not book_details.empty:
        book_title = book_details["Title"].iloc[0]
        if book_title not in titles_seen:  # Check if the title is already added
            book_info = {
                "ISBN": isbn,
                "Title": book_title,
                "Author": book_details["Author"].iloc[0],
                "Year": int(book_details["Year"].iloc[0]),
                "Publisher": book_details["Publisher"].iloc[0],
            }
            book_details_list.append(book_info)
            titles_seen.add(book_title)
            # print(book_info['Title'])
    else:
        print(f"Book with ISBN {isbn} not found.")
    count += 1

# If you still want to output JSON with the detailed list
output = json.dumps(
    {
        # "Input Book": bookName,
        "Recommended Books 7. Hybrid Approach (Content+Collaborative) Using percentile": book_details_list
    },
    ensure_ascii=False,
    indent=4,
)

print(output)
print("]")
