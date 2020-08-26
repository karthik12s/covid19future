from flask import Flask, redirect, url_for,session,request,render_template,session,flash
import requests
from sklearn import linear_model
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
wc=requests.get('https://api.covid19api.com/summary')
wc=wc.json()
ind=wc['Countries'][76]
s_d=(requests.get('https://api.covidindiatracker.com/state_data.json')).json()
app=Flask(__name__)
app.secret_key='abc'
a=requests.get('https://api.covid19india.org/states_daily.json')
a=a.json()
c=a['states_daily']
c=c[::3]
def date1(a):
    st=''
    if a<92:
        st=str(a[0]-60)+'-Mar-20'
        return st
    if a<122:
        st=str(a[0]-91)+'-Apr-20'
        return st
    if a<153:
        st=str(a[0]-121)+'-May-20'
        return st
    if a<184:
        st=str(a[0]-152)+'-Jun-20'
        return st
    if a<214:
        st=str(a[0]-183)+'-Jul-20'
        return st
    if a<244:
        st=str(a[0]-213)+'-Aug-20'
        return st
    if a<274:
        st=str(a[0]-233)+'-Sep-20'
        return st
'''@app.route("/home")
@app.route("/")
def home():
	if "user" in session:
		return render_template('home.html',n=session["user"])
	return render_template('home.html')'''
@app.route("/")
@app.route("/<name>")
def page(name=None):
    if name==None:
        name='tt'
    if name in c[0]:
        st=[]
        day=[]
        for i in range(len(c)):
            st.append(c[i][name])
            day.append(i+75)
        day=(np.array(day)).reshape(-1,1)
        x1=(np.arange(75,len(day)+90)).reshape(-1,1)
        st=list(map(int,st))
        for i in range(1,len(st)):
            st[i]=st[i]+st[i-1]
        st=(np.array(st)).reshape(-1,1)
        mo=PolynomialFeatures(degree=5)
        new2=mo.fit_transform(day,st)
        xtt=mo.transform(x1)
        tt=linear_model.LinearRegression()
        tt.fit(new2,st)
        ytt=tt.predict(xtt)
        for i in range(len(ytt)):
            ytt[i]=int(ytt[i])
        if name=='tt':
            wc=[ind['TotalConfirmed'],ind['TotalDeaths'],ind['TotalRecovered'],ind['NewConfirmed']]
        else:
            for i in range(len(s_d)):
                if s_d[i]['state']==s_keys[name]:
                    wc=[s_d[i]['confirmed'],s_d[i]['deaths'],s_d[i]['recovered'],st[len(c)-1][0]]

        #ytt=list(map(int,ytt))
        return render_template('new.html',da=list(map(date1,x1)),y=ytt,r=len(day),or1=st,l=len(x1),d1=x1,labels=list(map(date1,x1))[::15],values=ytt[::15],max=max(ytt),values1=st[::15],im=stateDict[name],sn=namesDict[name],wc=wc,p=ytt[len(c)])
    else:
        return redirect(url_for('home'))


stateDict={"an":"https://www.youngernation.com/wp-content/uploads/2017/12/Andaman.jpg","ap":"https://www.youngernation.com/wp-content/uploads/2017/12/Andhra-1.jpg","ar":"https://www.youngernation.com/wp-content/uploads/2017/12/Arunachal-1.jpg","as":"https://www.youngernation.com/wp-content/uploads/2017/12/Assam-1.jpg","br":"https://www.youngernation.com/wp-content/uploads/2017/12/Bihar-1.jpg","ch":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-Union-Territory-Chandigarh.jpg","ct":"https://www.youngernation.com/wp-content/uploads/2017/12/Chhattisgarh-1.jpg","dd":"https://www.youngernation.com/wp-content/uploads/2017/12/Daman-and-Diu.jpg",'dl':'https://cdn.sketchbubble.com/pub/media/catalog/product/optimized1/a/1/a1d5257e10517b286ca194ca176c63bafc47774022219aef1b2db50a81b07bd6/delhi-map-slide1.png',"dn":"https://www.youngernation.com/wp-content/uploads/2017/12/Dadra-and-Nagar-Haveli.jpg","ga":"https://www.youngernation.com/wp-content/uploads/2017/12/Goa-1.jpg","gj":"https://www.youngernation.com/wp-content/uploads/2017/12/Gujarat.jpg","hp":"https://www.youngernation.com/wp-content/uploads/2017/12/Himachal-1.jpg","hr":"https://www.youngernation.com/wp-content/uploads/2017/12/Haryana-1.jpg","jh":"https://www.youngernation.com/wp-content/uploads/2017/12/Jharkhand-1.jpg","jk":"https://thumbs.dreamstime.com/b/web-155417042.jpg","ka":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Karnataka.jpg","kl":"https://www.youngernation.com/wp-content/uploads/2017/12/Kerala.jpg","la":"https://www.youngernation.com/wp-content/uploads/2017/12/Lakhadeep.jpg","ld":"https://thumbs.dreamstime.com/b/web-155417042.jpg","me":"https://www.youngernation.com/wp-content/uploads/2017/12/Meghalaya-1.jpg","mh":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Maharashtra.jpg","mn":"https://www.youngernation.com/wp-content/uploads/2017/12/Manipur-1.jpg","mp":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Madhya-Pradesh.jpg","mz":"https://www.youngernation.com/wp-content/uploads/2017/12/Mizoram-1.jpg","nl":"https://www.youngernation.com/wp-content/uploads/2017/12/Nagaland-1.jpg","or":"https://www.youngernation.com/wp-content/uploads/2017/12/Odisha.jpg","pb":"https://www.youngernation.com/wp-content/uploads/2017/12/Punjab-1.jpg","py":"https://www.youngernation.com/wp-content/uploads/2017/12/Puducherry.jpg","rj":"https://www.youngernation.com/wp-content/uploads/2017/12/Rajasthan.jpg","sk":"https://www.youngernation.com/wp-content/uploads/2017/12/Sikkim-1.jpg","tg":"https://www.youngernation.com/wp-content/uploads/2017/12/Telangana-1.jpg","tn":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Tamil-Nadu.jpg","tr":"https://www.youngernation.com/wp-content/uploads/2017/12/Tripura-1.jpg",'tt':'https://fvmstatic.s3.amazonaws.com/maps/m/IN-EPS-02-4001.png',"up":"https://www.youngernation.com/wp-content/uploads/2017/12/Uttar-Pradesh.jpg","ut":"https://www.youngernation.com/wp-content/uploads/2017/12/Uttarakhand-1.jpg","wb":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-West-Bengal.jpg"}
namesDict ={'an':'Andaman And Nicobar','ap': 'Andhra Pradesh','ar' :'Arunachal Pradesh','as'  : 'Assam','br' :'Bihar','ch': 'Chandigarh','ct' :'Chattisgarh','dd': 'Daman & Diu','dl' :'Delhi','dn' : 'Dardar and Nagar Haveli','ga': 'Goa','gj' :'Gujarath','hp' :'Himachal Pradesh','hr' : 'Haryana','jh' :'Jarkhand','jk': 'Jammu And Kashmir','ka': 'Karnataka','kl': 'Kerala','ld' : 'Ladakh','la': 'Lakshwadeep','mh': 'Maharashtra','me': 'Meghalaya','mn': 'Manipur','mp' : 'Madhya Pradesh','mz': 'Mizoram','nl': 'Nagaland','or': 'Orissa','pb': 'Punjab','py' :'Pondicherry','rj': 'Rajasthan','sk': 'Sikkim','tg': 'Telangana','tn': 'TamilNadu','tt':'India','tr' :'Tripura','up' :'UttarPradesh','ut': 'Uttarakand','wb' :'WestBengal','tt': 'Total'}

li=['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bolivia (Plurinational State of)', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'China, Hong Kong SAR', 'China, Macao SAR', 'China, mainland', 'China, Taiwan Province of', 'Colombia', 'Congo', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', "Democratic People's Republic of Korea", 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'United Republic of Tanzania', 'United States of America', 'Uruguay', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe']
s_names=[ 'Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Daman & Diu', 'Delhi','Dardar and Nagar Haveli', 'Goa', 'Gujarath', 'Himachal Pradesh','Haryana', 'Jarkhand', 'Jammu And Kashmir', 'Karnataka', 'Kerala','Ladakh', 'Lakshwadeep', 'Maharashtra', 'Meghalaya', 'Manipur','Madhya Pradesh', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab','Pondicherry', 'Rajasthan', 'Sikkim', 'Telangana', 'TamilNadu','Tripura', 'UttarPradesh', 'Uttarakand', 'WestBengal', 'India']
s_keys={'an':'Andaman and Nicobar Islands', 'ap':'Andhra Pradesh', 'ar':'Arunachal Pradesh', 'as':'Assam', 'br':'Bihar', 'ch':'Chhattisgarh', 'ct':'Chandigarh', 'dd':'Daman and Diu', 'dl':'Delhi', 'dn':'Dadra and Nagar Haveli', 'ga':'Goa', 'gj':'Gujarat', 'hp':'Himachal Pradesh', 'hr':'Haryana', 'jh':'Jharkhand', 'jk':'Jammu and Kashmir', 'ka':'Karnataka', 'kl':'Kerala', 'la':'Ladakh', 'ld':'Lakshadweep', 'mh': 'Maharashtra', 'ml':'Meghalaya', 'mn':'Manipur', 'mp':'Madhya Pradesh', 'mz':'Mizoram', 'nl':'Nagaland', 'or':'Odisha', 'pb':'Punjab', 'py':'Puducherry', 'rj':'Rajasthan', 'sk':'Sikkim', 'tg':'Telangana', 'tn':'Tamil Nadu', 'tr':'Tripura','up':'Uttar Pradesh', 'ut':'Uttarakhand', 'wb':'West Bengal'}
if __name__=='__main__':
	app.run(debug=True)
