
# Load EDA
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


# Load Our Dataset
def load_data(data):
	df = pd.read_csv(data)
	return df


# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(data):
	count_vect = CountVectorizer()
	cv_mat = count_vect.fit_transform(data)
	# Get the cosine
	cosine_sim_mat = cosine_similarity(cv_mat)
	return cosine_sim_mat

def get_recommendation(title,cosine_sim_mat,df,num_of_rec=10):
	# indices of the course
	course_indices = pd.Series(df.index,index=df['course_title']).drop_duplicates()
	# Index of course
	idx = course_indices[title]

	# Look into the cosine matr for that index
	sim_scores =list(enumerate(cosine_sim_mat[idx]))
	sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)
	selected_course_indices = [i[0] for i in sim_scores[1:]]
	selected_course_scores = [i[0] for i in sim_scores[1:]]

	# Get the dataframe & title
	result_df = df.iloc[selected_course_indices]
	result_df['similarity_score'] = selected_course_scores
	final_recommended_courses = result_df[['course_title','similarity_score','url','price','num_subscribers']]
	return final_recommended_courses.head(num_of_rec)



def search_term_if_not_found(term,df):
	result_df = df[df['course_title'].str.contains(term,case=False)]
	return result_df

def search_based_on_intreset_domain(df,domain,interest):
	domain_df = df[df['subject']==domain]
	sorted_df = domain_df.sort_values(by=['num_subscribers'], ascending=False)
	filtered_df = df[df['course_title'].str.contains(interest,case=False)].head(3)
	filtered_res = filtered_df.to_json(orient='records')[1:-1].replace('},{', '} {')
	return filtered_res

def main():


	df = load_data(r"C:\py\blog-master\blog-master\rasa\udemy_data\udemy_courses.csv")
	cosine_sim_mat = vectorize_text_to_cosine_mat(df['course_title'])
	search_term = "python"
	try:
		results = get_recommendation("search_term",cosine_sim_mat,df,10)
		print(results)

	except:
		results= "Not Found"
		# result_df = search_term_if_not_found(search_term,df)
		result_df = search_based_on_intreset_domain(df,"Business Finance","python")
		print(result_df)



				# How To Maximize Your Profits Options Tradin


if __name__ == '__main__':
	main()