import readdata
import json

review_file = 'reviews_Cell_Phones_and_Accessories.json.gz'
review_feature_file = 'review_features.txt'
review_text_file = 'review_text.txt'

def extractReviewFeatures(review):
  product_id = review['asin']
  reviewer_id = review['reviewerID']
  review_text = review['reviewText']
  review_summary = review['summary'] 
  review_text_len = len(review_text)
  review_score = review['overall']
  review_time = review['unixReviewTime'] # will give us position
  review_num_feedbacks = review['helpful'][0]
  review_pos_feedbacks = review['helpful'][0]
    # need to store how many positive ahead and negative revivews before
    
  try:
    reviewer_name = review['reviewerName']
  except KeyError:
    reviewer_name = ""

  return (product_id + ", " + reviewer_id + ", " + \
            reviewer_name + ", " + str(review_text_len) + ", " + \
            str(review_num_feedbacks) + ", " + str(review_pos_feedbacks) + ", " + \
            str(review_score) + ", " + review_summary + ", " + str(review_time) )


#rtf = open(review_text_file, 'wt')
rff = open(review_feature_file, 'wt')      
for line in readdata.parse(review_file):
  review = readdata.dataInJson(line)
  if review is not None:
    review_features = extractReviewFeatures(review)
    if review_features is not None:
      rff.write(review_features)

