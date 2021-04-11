
# coding: utf-8

# In[1]:


import sys
import pandas as pd
from pandas import Series, DataFrame
import re
import numpy as np
from requests import get
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from datetime import date,timedelta,datetime
import time
import json
import calendar
import math
from konlpy.tag import Twitter as original_Twitter
from ckonlpy.tag import Twitter
from bom_text_preprocessor import BOM_EMOJI
from bom_text_preprocessor import emoji2text
from bom_text_preprocessor import dataframe2json
from bom_text_preprocessor import pnormalizer # 'gl','powder','meme'
from pymongo import MongoClient


# In[2]:


client=MongoClient("mongodb://pungdeong:pungdeong@13.125.143.101/pungdeongBOM")
db = client.pungdeongBOM
raw_product_DB=db.product_DB
raw_normalizer=db.normalizer
ex_product_DB = pd.Series([doc for doc in raw_product_DB.find()])
ex_normalizer = pd.Series([doc for doc in raw_normalizer.find()])


# In[3]:


# 데이터 프레임화
# normalizer
nor_brandname=[ex_normalizer[i]['brandname'] for i in range(len(ex_normalizer))]
nor_origin=[ex_normalizer[i]['origin'] for i in range(len(ex_normalizer))]
nor_pname=[ex_normalizer[i]['pname'] for i in range(len(ex_normalizer))]
nor_site=[ex_normalizer[i]['site'] for i in range(len(ex_normalizer))]
# product_DB
pdb_brandname=[ex_product_DB[i]['product']['brandname'] for i in range(len(ex_product_DB))]
pdb_category=[ex_product_DB[i]['product']['category'] for i in range(len(ex_product_DB))]
pdb_gl_num_rev=[ex_product_DB[i]['product']['gl_num_rev'] for i in range(len(ex_product_DB))]
pdb_origin_id=[ex_product_DB[i]['product']['origin_id'] for i in range(len(ex_product_DB))]
pdb_pid=[ex_product_DB[i]['product']['pid'] for i in range(len(ex_product_DB))]
pdb_pname=[ex_product_DB[i]['product']['pname'] for i in range(len(ex_product_DB))]
pdb_product_attribute=[ex_product_DB[i]['product']['product_attribute'] for i in range(len(ex_product_DB))]
pdb_product_desc=[ex_product_DB[i]['product']['product_desc'] for i in range(len(ex_product_DB))]
pdb_product_price=[ex_product_DB[i]['product']['product_price'] for i in range(len(ex_product_DB))]
pdb_product_volume=[ex_product_DB[i]['product']['product_volume'] for i in range(len(ex_product_DB))]
pdb_sales=[ex_product_DB[i]['product']['sales'] for i in range(len(ex_product_DB))]
pdb_review=[ex_product_DB[i]['review'] for i in range(len(ex_product_DB))]
pdb_user=[ex_product_DB[i]['user'] for i in range(len(ex_product_DB))]


# In[6]:


data=pd.DataFrame(
    {'brandname':nor_brandname,
    'origin':nor_origin,
    'pname':nor_pname,
    'site':nor_site})
normalizer_df=DataFrame(data)
normalizer_df=DataFrame(data, columns=['brandname',"origin",'pname','site'])

data = pd.DataFrame(
            {'brandname': pdb_brandname,
            'category': pdb_category,
             'gl_num_rev' : pdb_gl_num_rev,
             'origin_id':pdb_origin_id,
             'pid':pdb_pid,
             'pname':pdb_pname,
             'product_attribute':pdb_product_attribute,
             'product_desc':pdb_product_desc,
             'product_price':pdb_product_price,
             'product_volume':pdb_product_volume,
             'sales':pdb_sales,
             'review':pdb_review,
             'user':pdb_user
            })
product_df=DataFrame(data)
product_df=DataFrame(data, columns=['brandname',"category",'gl_num_rev','origin_id','pid','pname','product_attribute','product_desc','product_price','product_volume','sales','review','user'])


# In[7]:


# load essential data
# 데이터프레임형태
product_DB = product_df
normalizer = normalizer_df


# In[8]:


########################################## 크롤링 코드 ###############################


# In[9]:


score_dict = {'worst': 1, 'bad': 2, 'soso': 3, 'good': 4, 'best':5}
pd_c_list={100:"모공",200:"각질",300:"주름",400:"잡티",500:"건조함",600:"피부톤",700:"민감성",800:"트러블",900:"아토피",1000:"피지과다"}
pd_s_type={100:"건성",200:"중성",300:"지성",400:"복합성"}
mm_score_dic ={"":0,"half":0.5,"one":1,"oneHalf":1.5,"two":2,"twoHalf":2.5,"three":3,"threeHalf":3.5,"four":4,"fourHalf":4.5,"five":5} 
    # 별점이 숫자가 아닌 텍스트로 되어있음. 텍스트에 대응되는 별점 딕셔너리


# In[10]:


# 별의 텍스트를 뽑아내는 함수  
def mm_starnum(star):
    first=0
    second=0
    for i in range(len(star)):
        if star[i]=="\"":
            if first==0:
                first=i
            else: 
                second=i
    return star[first+1:second]
# 날짜 텍스트를 변환해주는 함수
def date_transfer(date_info):
    
    year=int(str(datetime.today())[:4]) # 오늘 년
    month=int(str(datetime.today())[5:7]) # 오늘 월
    day=int(str(datetime.today())[8:10]) # 오늘 일 
    
    if "초 전" in date_info or "초전" in date_info:
        n_date=date(year,month,day)
        n_date='{:%Y-%m-%d}'.format(n_date)
    
    elif "분 전" in date_info or "분전" in date_info:
        n_date=date(year,month,day)
        n_date='{:%Y-%m-%d}'.format(n_date)
        
    elif "시간 전" in date_info or "시간전" in date_info:
        n_date=date(year,month,day)
        n_date='{:%Y-%m-%d}'.format(n_date)

    
    elif "일 전" in date_info or "일전" in date_info:
        d_day=int(re.sub("[^0-9]","",date_info))
        if (day-d_day)>=1:
            n_date=date(year,month,(day-d_day))
            n_date='{:%Y-%m-%d}'.format(n_date)

        else:
            lastday=calendar.monthrange(year,month-1)[1]
            temp=lastday-d_day
            n_date=date(year,(month-1),(temp+day))
            n_date='{:%Y-%m-%d}'.format(n_date)
      

    elif "개월 전" in date_info or "개월전" in date_info:
        n_month=int(re.sub("[^0-9]","",date_info)) # 몇 달전 인지
        
        if (month-n_month)>=1:
            n_date=date(year,(month-n_month),day)
            n_date='{:%Y-%m-%d}'.format(n_date)

        else:
            temp=12-n_month
            n_date=date(year,(temp+month),day)
            n_date='{:%Y-%m-%d}'.format(n_date)

    else:
        n_date=date_info
        
    return n_date


# In[11]:


meme_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/memebox/meme_id.csv')
gl_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/glowpick/gl_id.csv')
pod_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/powderroom/pod_id.csv')


# In[12]:


# 뷰티 리뷰 사이트에 원하는 제품을 입력하면 리뷰를 주기적으로 가져오는 크롤러
# 미미박스, 글로우픽, 파우더룸
# 모든 제품 리뷰를 실시간으로 가져옴 

class bom_crawler():
    import sys
    import pandas as pd
    from pandas import Series, DataFrame
    import re
    import numpy as np
    from requests import get
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    from datetime import date,timedelta,datetime
    import time
    import json
    import calendar
    import math

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    t_date=datetime.today().strftime('%Y-%m-%d') # 오늘 
    yesterday = date.today() - timedelta(1)
    y_date=yesterday.strftime('%Y-%m-%d') # 어제

    def __init__(self): # 인스턴스 속성- 변수에 들어가있는 값이 클래스 별로 다르다.
        #product
        self.pid=[] # 제품 id - int 
        self.pname=[] # 제품 이름 - string
        self.brandname=[] # 브랜드이름 - string
        self.category=[] # 제품 카테고리 - string
     
        # user
        self.age=[] # 나이 - int
        self.concern_list=[] # 피부고민 - list[string]
        self.skin_type=[] # 피부타입 - string
        self.repurchased=[] # 재구매여부 - boolean

        # review
        self.d_date=[] # 리뷰 생성날짜 - datetime
        self.score=[] # 리뷰 평점 - float
        self.like_c=[] # 좋아요개수 - int
        self.tags=[] # 제품태그 - list[string]
        self.text=[] # 리뷰 - string

    ## 클래스 메소드
    # @classmethod 

    ### 인스턴스 메소드 

    # 미미박스 크롤링함수
    def meme_review_crawl(self):
        for p_id in meme_id['pid']:
            url = 'https://www.memebox.com/ajax/reviews?productId='+str(p_id)+'&orderType=createdatDESC&page=1&contentViewPickOption=all'
            html = get(url,headers=self.headers).text
            soup = bs(html,'lxml')
            print(url)
            print("****************************************************")
            for k in range(len(soup.select('body > form > div.view'))):
                r_date=date_transfer(soup.select('div.info')[k].select('span.date')[0].text)
                if r_date==self.t_date or r_date==self.y_date: # 리뷰 날짜가 오늘이나 어제와 같다면
                    
                    ### product
                    self.pid.append(meme_id.loc[meme_id.pid==p_id,'pid'].values[0]) # item_id
                    self.pname.append(meme_id.loc[meme_id.pid==p_id,'pname'].values[0])# item_name
                    self.brandname.append(meme_id.loc[meme_id.pid==p_id,'brandname'].values[0])# brand_name
                    self.category.append(meme_id.loc[meme_id.pid==p_id,'category'].values[0])# category
                     
                    #review
                    # date 아래에 
                    self.score.append(mm_score_dic[mm_starnum(str(soup.select('span.star > em')[k]))]) # 리뷰 평점
                    self.like_c.append(re.sub("\n| ","",soup.select('span.like-thumb-text')[k].text))  # 리뷰 좋아요 개수
                    self.tags.append(" ") # 태그
                    self.text.append(re.sub('\t','',soup.select('div > p.reviews-written-text-deal-detail')[k].text).strip()) # 리뷰 텍스트

                    
                    ### user
                    self.age.append(" ")# 나이 
                    if len(soup.select('div.info')[k].select('span'))==2: #  피부타입 & 리뷰 작성일
                        self.skin_type.append(re.sub("/","",soup.select('div.info')[k].select('span')[0].text).strip())  
                        self.d_date.append(r_date)
                    else:
                        self.skin_type.append(" ") 
                        self.d_date.append(r_date)
                    self.concern_list.append(" ")# 피부고민    
                    if soup.select('div.review-selected-option')[k].select('span'): # 재구매 여부
                        self.repurchased.append(soup.select('div.review-selected-option')[k].select('span')[0].text)
                    else:
                        self.repurchased.append(" ")

    
    # 파우더룸 크롤링함수
    def powder_review_crawl(self):
        for p_id in pod_id['pid']:
            url='https://www.powderroom.co.kr/api/products/'+str(p_id)+'/reviews?order=new'
            html=get(url,headers=self.headers).text
            reviews=json.loads(html)
            print(url)
            print("****************************************************")
            for i in range(len(reviews)):
                date_result=pd.to_datetime(str(reviews[i]['$created'])[:-3],unit='s')
                r_date=date_result.strftime('%Y-%m-%d')      
                if r_date==self.t_date or r_date==self.y_date: # 리뷰 날짜가 오늘이나 어제와 같다면

                    ### product
                    self.pid.append(p_id) # 제품 id
                    self.pname.append(str(pod_id.loc[pod_id.pid==int(p_id),'pname'].values)[2:-2]) # 제품 이름
                    self.brandname.append(str(pod_id.loc[pod_id.pid==int(p_id),'brandname'].values)[2:-2]) #브랜드 이름
                    self.category.append(str(pod_id.loc[pod_id.pid==int(p_id),'category'].values)[2:-2]) #카테고리

                    ### review 

                    self.d_date.append(r_date) # date
                    self.score.append(reviews[i]['rate'])# score 
                    self.like_c.append(reviews[i]['count']['like'])# like_c
                    self.tags.append(reviews[i]['tags'])# tags 
                    self.text.append(reviews[i]['text']) # 텍스트 
                   
                    
                    ### user        
                    try: # json에 age 키 값이 없는 경우가 있다. (사이트에는 있음)
                        self.age.append(reviews[i]['user']['age']) # 나이 
                    except:
                        self.age.append(" ")
                    try: # 피부 타입
                        self.skin_type.append(pd_s_type[reviews[i]['user']['skin']['type']])# skin_type
                    except:
                        self.skin_type.append(" ") 

                    tmp_c_list=[]
                    try: # 피부고민, 
                        for a in reviews[i]['user']['skin']['concerns']:
                            tmp_c_list.append(pd_c_list[a])
                        self.concern_list.append(",".join(tmp_c_list))
                    except:
                        self.concern_list.append(" ") 

                    self.repurchased.append(reviews[i]['repurchased'])# repurchase
    # 글로우픽 크롤링 함수            
    def glowpick_review_crawl(self):
        chrome_path = 'C:/Users/Ilhoon/Desktop/dev_util/chromedriver_win32/chromedriver'
        options=webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(chrome_path, chrome_options=options)

        for p_id in gl_id["pid"]:
            time.sleep(1)
            driver.get('http://glowpick.com/product/'+str(p_id)+'')
            html = driver.page_source
            soup = bs(html, 'lxml')
            print('http://glowpick.com/product/'+str(p_id)+'')
            print("****************************************************")

            for k in range(len(soup.select('section.section-list-item > ul.review-list-wrap > li'))):
                r_date=re.sub("[^0-9]","-",date_transfer(soup.select('section.section-list-item > ul.review-list-wrap > li > span.date')[k].text))   
                if r_date==self.t_date or r_date==self.y_date: # 리뷰 날짜가 오늘이나 어제와 같다면
                        
                    ### product 
                    self.pid.append(p_id) # 제품 id 
                    self.pname.append(gl_id.loc[gl_id.pid==p_id,'pname'].values[0]) # 제품 이름
                    self.brandname.append(gl_id.loc[gl_id.pid==p_id,'brandname'].values[0]) # 브랜드 이름
                    self.category.append(gl_id.loc[gl_id.pid==p_id,'category'].values[0]) # 카테고리
                    
                    ### review
                    self.d_date.append(r_date) # 날짜 정보
                    self.score.append(score_dict[soup.select('div > div > div > p > span.info > span.label > span')[k*2]['class'][1][4:]])# 점수
                    self.like_c.append(" ") # 좋아요개수 
                    self.tags.append(" ") # 태그
                    self.text.append(soup.select('section.section-list-item > ul.review-list-wrap > li > div > p')[k].text)    # 리뷰 텍스트
                
                    
                    ### user
                    self.age.append(soup.select('section.section-list-item > ul.review-list-wrap > li > div > div > div > p > span.info > span.txt')[k].text[:3]) # 나이
                    self.skin_type.append(re.sub("·","",soup.select('section.section-list-item > ul.review-list-wrap > li > div > div > div > p > span.info > span.txt')[k].text[4:]).strip()) # 피부타입
                    self.concern_list.append(" ") # 피부고민
                    self.repurchased.append(" ") # 재구매
                    
                    # 유저 이름
                    # self.user_name.append(soup.select('section.section-list-item > ul.review-list-wrap > li > div > div > div > p > span.name')[k].text)
                     
    # 리스트들의 길이를 체크
    def chk_len(self):
        print(len(self.pid))
        print(len(self.pname))
        print(len(self.brandname))
        print(len(self.age))
        print(len(self.tags))
        print(len(self.repurchased))
        print(len(self.like_c))
        print(len(self.category))
        print(len(self.skin_type))
        print(len(self.score))
        print(len(self.d_date))
        print(len(self.text))
        print(len(self.concern_list))
        
    def printclass(self):
        print(self.headers)
    
    # 데이터 프레임을 만드는 함수
    def get_df(self):
        data = self.pd.DataFrame(
            {'brandname': self.brandname,
            'pid': self.pid,
             'pname' : self.pname,
             'age':self.age,
             'tags':self.tags,
             'repurchased':self.repurchased,
             'like_c':self.like_c,
             'category':self.category,
             'concern_list':self.concern_list,
             'skin_type':self.skin_type,
             'score':self.score,
             'date':self.d_date,
             'text':self.text
            })
        self.result_df=DataFrame(data)
        self.result_df=DataFrame(data, columns=['category','brandname',"pid",'pname','age','tags','repurchased','like_c','concern_list','skin_type','score','date','text'])
        return self.result_df
        #print(result_df)
    


# In[11]:


# memebox.result_df=memebox.result_df.loc[:,('category','brandname','pid','pname','score','text','date','like_c','skin_type','requrchased')]
# powderroom.result_df=powderroom.result_df.loc[:,('brandname',"pid",'pname','age','tags','repurchased','like_c','concern_list','skin_type','score','date','text')]


# In[12]:


# 리뷰간 중복을 제거하는 함수, 중복이 제거된 데이터 프레임만 qwe에 저장
# 크롤링한 리뷰들을 병합 + 글로우픽 추가 필요

# merged_df=pd.concat([memebox.result_df,powderroom.result_df])

# raw_tier1=db.raw_review_tier1
# ex_raw_tier1 = pd.Series([doc for doc in raw_tier1.find()])
# tt_date=datetime.today().strftime('%Y-%m-%d') # 오늘 
# yesterday = date.today() - timedelta(1)
# yy_date=yesterday.strftime('%Y-%m-%d') # 어제
# raw1_brandname=[]
# raw1_pname=[]
# raw1_date=[]
# raw1_text=[]

# for i in range(len(ex_raw_tier1)):
#     date_A=re.sub("[^0-9]","-",date_transfer(ex_raw_tier1[i]['review']['date']))
#     if date_A==tt_date or date_A==yy_date:
#         raw1_brandname.append(ex_raw_tier1[i]['product']['brandname'])
#         raw1_pname.append(ex_raw_tier1[i]['product']['pname'])
#         raw1_date.append(date_A)
#         raw1_text.append(ex_raw_tier1[i]['review']['text'])

# data = pd.DataFrame({'brandname':raw1_brandname,'pname' : raw1_pname,'date':raw1_date,'text':raw1_text})
# saved_df=DataFrame(data)
# saved_df=DataFrame(data, columns=['brandname','pname','date','text'])
# qwe=pd.concat([merged_df,saved_df])
# qwe=qwe.drop_duplicates(['date','text','pname'])


# In[13]:


# #### customized_twitter tokenizer
# # 브랜드 이름 명사로 저장


# brand_set = np.array([re.sub('[^가-힣]','',x) for x in product_DB.brandname.unique()])
# brand_set = pd.Series([x for x in brand_set if x != ''])

# # 특수 이름 추가
# brand_set = brand_set.append(pd.Series(['비씨데이션','파데','다크닝','지속력','밀착력','피부톤','커버력','쿨톤','웜톤','결보정','코끼임']),ignore_index=True)

# # 트위터 tokenizer loading 및 업로드
# twitter = Twitter()
# twitter.add_dictionary(brand_set,'Noun')

# # 원래 tokenizer 업로드
# ori_twitter = original_Twitter()
# #### emoji2text
# preprocessed_text = emoji2text(review_DB.text)
# #### upper & 제품 매핑
# preprocessed_text = pd.Series(preprocessed_text).apply(lambda x:x.upper())
# #### twitter tokenizing 명사는 customized 나머지는 original
# bow = preprocessed_text.apply(lambda x:','.join([ori_twitter.pos(token,stem=True,norm=True)[0][0] if pos in ['Adjective','Verb'] else token for token, pos in twitter.pos(x) if pos in ['Noun','Adjective','Verb','Alpha']]))


# In[14]:


# #### add tokens to dataframe
# review_DB['text_token'] = bow


# In[15]:



# review_DB['origin']=review_DB['pname']
# review_DB['origin_id']=review_DB['pid']
# review_DB=review_DB.drop(['brandname','pname','pid','category'],axis=1)
# temp=pd.merge(normalizer,review_DB,on='origin')
# temp
# temp=temp.drop('brandname',axis=1)
# result=pd.merge(product_DB,temp,on='pname')

# product = ["pid", "pname", "product_desc", "product_attribute", "product_volume", "product_price", "sales", "brandname",'category','origin_id']
# user_info = ['age','skin_type','concern_list','repurchased']
# review = ['date','score','text','text_token','tags']

# result = dataframe2json(result,product,user_info,review)

# for x in range(len(result)):
#     result[x]['product']['origin_id'] = int(result[x]['product']['origin_id']) 
#     result[x]['user']['repurchased'] = int(re.sub(' ','0',str(result[x]['user']['repurchased'])))
#     #result[x]['user']['repurchased']=int(result[x]['user']['repurchased'])
#     result[x]['review']['score'] = int(result[x]['review']['score'])
        


# In[16]:


# #### mongoDB저장 코드
# client = MongoClient("mongodb://pungdeong:pungdeong@13.125.143.101/pungdeongBOM")
# db = client.pungdeongBOM
# raw_review = db.raw_review_tier1 #요 collection에 쌓아라.
# raw_review.insert_many(result)


# In[13]:


# 파이썬 파일을 실행할때 실행하고 싶은 명령 모두 아래에 입력
if __name__ == "__main__":
    
    # 사이트를 BOM_crawler 인스턴스로 할당
    memebox=bom_crawler()
    powderroom=bom_crawler()
    glowpick=bom_crawler()
    
    # id를 불러옴 
    meme_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/memebox/meme_id.csv')
    gl_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/glowpick/gl_id.csv')
    pod_id = pd.read_csv('C:/Users/Ilhoon/Anaconda_project/ebiz_CAPSTONE/crawling/powderroom/pod_id.csv')
    
    # 사이트별 리뷰 크롤링
    powderroom.powder_review_crawl()
    memebox.meme_review_crawl()
    glowpick.glowpick_review_crawl()
    # 크롤링한 데이터 프레임 저장
    powderroom.get_df()
    memebox.get_df()
    glowpick.get_df()
    
    
    # crawled data set / 중복을제거
    # 6/6 새로 추가된 데이터
    #************************ 이후 부터는 중복을 제거한 리뷰만 넣기 위해 review_DB=qwe로 변경
    # 리뷰간 중복을 제거하는 함수, 중복이 제거된 데이터 프레임만 qwe에 저장
    # 크롤링한 리뷰들을 병합 + 글로우픽 추가 필요

    merged_df=pd.concat([memebox.result_df,powderroom.result_df])
    raw_tier1=db.raw_review_tier1
    ex_raw_tier1 = pd.Series([doc for doc in raw_tier1.find()])
    tt_date=datetime.today().strftime('%Y-%m-%d') # 오늘 
    yesterday = date.today() - timedelta(1)
    yy_date=yesterday.strftime('%Y-%m-%d') # 어제
    raw1_brandname=[]
    raw1_pname=[]
    raw1_date=[]
    raw1_text=[]

    for i in range(len(ex_raw_tier1)):
        date_A=re.sub("[^0-9]","-",date_transfer(ex_raw_tier1[i]['review']['date']))
        if date_A==tt_date or date_A==yy_date:
            raw1_brandname.append(ex_raw_tier1[i]['product']['brandname'])
            raw1_pname.append(ex_raw_tier1[i]['product']['pname'])
            raw1_date.append(date_A)
            raw1_text.append(ex_raw_tier1[i]['review']['text'])

    data = pd.DataFrame({'brandname':raw1_brandname,'pname' : raw1_pname,'date':raw1_date,'text':raw1_text})
    saved_df=DataFrame(data)
    saved_df=DataFrame(data, columns=['brandname','pname','date','text'])
    qwe=pd.concat([merged_df,saved_df])
    qwe=qwe.drop_duplicates(['date','text','pname'])

    review_DB=qwe
    
    #### customized_twitter tokenizer
    # 브랜드 이름 명사로 저장


    brand_set = np.array([re.sub('[^가-힣]','',x) for x in product_DB.brandname.unique()])
    brand_set = pd.Series([x for x in brand_set if x != ''])

    # 특수 이름 추가
    brand_set = brand_set.append(pd.Series(['비씨데이션','파데','다크닝','지속력','밀착력','피부톤','커버력','쿨톤','웜톤','결보정','코끼임']),ignore_index=True)

    # 트위터 tokenizer loading 및 업로드
    twitter = Twitter()
    twitter.add_dictionary(brand_set,'Noun')

    # 원래 tokenizer 업로드
    ori_twitter = original_Twitter()
    #### emoji2text
    preprocessed_text = emoji2text(review_DB.text)
    #### upper & 제품 매핑
    preprocessed_text = pd.Series(preprocessed_text).apply(lambda x:x.upper())
    
    bow = preprocessed_text.apply(lambda x:'◈'.join([token+ '╹' + pos if pos in ['Noun'] else ori_twitter.pos(token,stem=True,norm=True)[0][0]+'╹'+ori_twitter.pos(token,stem=True,norm=True)[0][1] for token, pos in twitter.pos(x)]))
    ### token normalizing 
    p_normal = {'BB╹Alpha':'비비크림╹Noun', 'CC╹Alpha':'씨씨크림╹Noun','비비╹Noun':'비비크림╹Noun','씨씨╹Noun':'씨씨크림╹Noun'
                ,'파데╹Noun':'파운데이션╹Noun','쟂빛╹Noun':'잿빛╹Noun','비씨╹Noun':'비씨데이션╹Noun'}
    bow = bow.apply(lambda x: '◈'.join([p_normal[token] if token in p_normal.keys() else token for token in x.split('◈')]))
    #### add tokens to dataframe
    review_DB['text_token'] = bow
    
    
    
    review_DB['origin']=review_DB['pname']
    review_DB['origin_id']=review_DB['pid']
    review_DB=review_DB.drop(['brandname','pname','pid','category'],axis=1)
    temp=pd.merge(normalizer,review_DB,on='origin')
    temp
    temp=temp.drop('brandname',axis=1)
    result=pd.merge(product_DB,temp,on='pname')

    product = ["pid", "pname", "product_desc", "product_attribute", "product_volume", "product_price", "sales", "brandname",'category','origin_id']
    user_info = ['age','skin_type','concern_list','repurchased']
    review = ['date','score','text','text_token','tags']

    result = dataframe2json(result,product,user_info,review)

    for x in range(len(result)):
        result[x]['product']['origin_id'] = int(result[x]['product']['origin_id']) 
        result[x]['user']['repurchased'] = int(re.sub(' ','0',str(result[x]['user']['repurchased'])))
        #result[x]['user']['repurchased']=int(result[x]['user']['repurchased'])
        result[x]['review']['score'] = int(result[x]['review']['score'])
    
    print(result)
    #### mongoDB저장 코드
#     client = MongoClient("mongodb://pungdeong:pungdeong@13.125.143.101/pungdeongBOM")
#     db = client.pungdeongBOM
#     raw_review = db.raw_review_tier1 #요 collection에 쌓아라.
#     raw_review.insert_many(result)
    

