import streamlit as st
from textblob import TextBlob
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# get subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# get polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

# function to compute analysis
def getAnalysis(score):
  if score < 0 :
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'


def app():
  st.title("Sentiment Analysis")
  df_clean=st.session_state.test
  #st.write(df_clean)
  df_clean['Subjectivity'] = df_clean['Comment'].apply(getSubjectivity)
  df_clean['Polarity'] = df_clean['Comment'].apply(getPolarity)
  
  df_clean['Analysis'] = df_clean['Polarity'].apply(getAnalysis)
  #st.write(df_clean)

  # % Percentages:
  pcomments = df_clean[df_clean.Analysis == 'Positive']
  pcomments = pcomments['Comment']

  st.write('Positive: ' +str(round((pcomments.shape[0]/df_clean.shape[0])*100, 1))+ '%')

  ncomments = df_clean[df_clean.Analysis == 'Negative']
  ncomments = ncomments['Comment']

  st.write('Negative: ' +str(round((ncomments.shape[0]/df_clean.shape[0])*100, 1))+ '%')

  nucomments = df_clean[df_clean.Analysis == 'Neutral']
  nucomments = nucomments['Comment']

  st.write('Neutral: ' +str(round((nucomments.shape[0]/df_clean.shape[0])*100, 1))+ '%')

  # Value Count
  df_clean['Analysis'].value_counts

  # Plot
  fig = plt.figure(figsize = (10, 5))
  plt.title('Sentiment Analysis',fontsize=20)
  plt.xlabel('Sentiment',fontsize=20)
  plt.ylabel('Counts',fontsize=20)
  ax=(df_clean['Analysis'].value_counts(normalize=True).mul(100).round(1)).plot(kind= 'bar')
  for p in ax.patches:
    ax.annotate(
        str(p.get_height()), xy=(p.get_x() + 0.25, p.get_height() + 0.1), fontsize=20,ha='center', va='center',
                    xytext=(0, 8),textcoords='offset points'
    )
  st.pyplot(fig)

  # WordCloud
  fig = plt.figure(figsize = (10, 5))
  allWords = ' '.join( [cmts for cmts in df_clean['Comment']])
  wordCloud = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(allWords)

  plt.imshow(wordCloud, interpolation= 'bilinear')
  plt.axis('off')
  st.pyplot(fig)




  

  
   
