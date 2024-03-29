import requests
from sklearn import linear_model
from flask import Flask, redirect, url_for,session,request,render_template,session,flash
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
wc=requests.get('https://api.covid19api.com/summary')
wc=wc.json()
ind=wc['Countries'][76]
s_d=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
app=Flask(__name__)
app.secret_key='abc'
a=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
c=a[::3]
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
    if a<215:
        st=str(a[0]-183)+'-Jul-20'
        return st
    if a<246:
        st=str(a[0]-214)+'-Aug-20'
        return st
    if a<277:
        st=str(a[0]-245)+'-Sep-20'
        return st
    if a<308:
        st=str(a[0]-276)+'-Oct-20'
        return st
    if a<338:
        st=str(a[0]-307)+'-Nov-20'
        return st
    if a<368:
        st=str(a[0]-337)+'-Dec-20'
        return st
    if a<399:
        st=str(a[0]-367)+'-Jan-21'
        return st
    if a<430:
        st=str(a[0]-398)+'-Feb-21'
        return st
    if a<461:
        st=str(a[0]-429)+'-Mar-21'
        return st
    if a<488:
        st = str(a[0]-457)+'-April-21'
        return st
    if a<519:
        st = str(a[0]-487)+'-May-21'
        return st
    if a<551:
        st = str(a[0]-519)+'-June-21'
        return st
    if a<581:
        st = str(a[0]-548)+'-July-21'
        return st
    if a<612:
        st = str(a[0]-580)+'-August-21'
        return st

@app.route("/")
@app.route("/<name>")
def home(name=None):
    if name==None:
        name='tt'
    if name in namesDict:
        st=list(c[name.upper()])
        day=[]
        for i in range(len(st)):
            # st.append(c[i][name])
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
                if s_d['State'][i]==s_keys[name]:
                    wc=[s_d['Confirmed'][i],s_d['Deaths'][i],s_d['Recovered'][i],st[len(c)-1][0]-st[len(c)-2][0]]

        #ytt=list(map(int,ytt))
        for i in range(len(ytt)):
            if ytt[i]<0:
                ytt[i]=0
        return render_template('new.html',da=list(map(date1,x1)),y=ytt,r=len(day),or1=st,l=len(x1),d1=x1,labels=list(map(date1,x1))[::15],values=ytt[::15],max=max(ytt),values1=st[::15],im=stateDict[name],sn=namesDict[name],wc=wc,p=ytt[len(c)])
    else:
        return redirect(url_for('home'))

@app.route('/predictor')
def pred():
    l = []
    for name in s_codes1:
        # print(name)
        if name in namesDict:
                st=[]
                day=[]

                for i in range(len(c[name.upper()])):
                    c1=list(c[name.upper()])
                    st.append(c1[i])
                    day.append(i+75)
                day=(np.array(day)).reshape(-1,1)
                x1=(np.arange(75,len(day)+90)).reshape(-1,1)
                st=list(map(int,st))
                for i in range(1,len(st)):
                    st[i]=st[i]+st[i-1]
                st=(np.array(st)).reshape(-1,1)
                mo=PolynomialFeatures(degree=6)
                new2=mo.fit_transform(day,st)
                xtt=mo.transform(x1)
                tt=linear_model.LinearRegression()
                tt.fit(new2,st)
                ytt=tt.predict(xtt)
                for i in range(len(ytt)):
                    ytt[i]=int(ytt[i])
                    if name == 'an':
                        l.append({"Date":date1(x1[i]),name:ytt[i][0]})
                    else:
                        l[i][name] = ytt[i][0]
    return {"states_daily":l}

s_codes1 = ['an', 'ap', 'ar', 'as', 'br', 'ch', 'ct', 'dd', 'dl', 'dn','ga', 'gj', 'hp', 'hr', 'jh', 'jk', 'ka', 'kl', 'la', 'ld', 'mh','ml', 'mn', 'mp', 'mz', 'nl', 'or', 'pb', 'py', 'rj', 'sk', 'tg', 'tn', 'tr', 'tt', 'un', 'up', 'ut', 'wb']
# stateDict={"an":"https://www.youngernation.com/wp-content/uploads/2017/12/Andaman.jpg","ap":"https://www.youngernation.com/wp-content/uploads/2017/12/Andhra-1.jpg","ar":"https://www.youngernation.com/wp-content/uploads/2017/12/Arunachal-1.jpg","as":"https://www.youngernation.com/wp-content/uploads/2017/12/Assam-1.jpg","br":"https://www.youngernation.com/wp-content/uploads/2017/12/Bihar-1.jpg","ch":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-Union-Territory-Chandigarh.jpg","ct":"https://www.youngernation.com/wp-content/uploads/2017/12/Chhattisgarh-1.jpg","dd":"https://www.youngernation.com/wp-content/uploads/2017/12/Daman-and-Diu.jpg",'dl':'https://cdn.sketchbubble.com/pub/media/catalog/product/optimized1/a/1/a1d5257e10517b286ca194ca176c63bafc47774022219aef1b2db50a81b07bd6/delhi-map-slide1.png',"dn":"https://www.youngernation.com/wp-content/uploads/2017/12/Dadra-and-Nagar-Haveli.jpg","ga":"https://www.youngernation.com/wp-content/uploads/2017/12/Goa-1.jpg","gj":"https://www.youngernation.com/wp-content/uploads/2017/12/Gujarat.jpg","hp":"https://www.youngernation.com/wp-content/uploads/2017/12/Himachal-1.jpg","hr":"https://www.youngernation.com/wp-content/uploads/2017/12/Haryana-1.jpg","jh":"https://www.youngernation.com/wp-content/uploads/2017/12/Jharkhand-1.jpg","jk":"https://thumbs.dreamstime.com/b/web-155417042.jpg","ka":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Karnataka.jpg","kl":"https://www.youngernation.com/wp-content/uploads/2017/12/Kerala.jpg","la":"https://www.youngernation.com/wp-content/uploads/2017/12/Lakhadeep.jpg","ld":"https://thumbs.dreamstime.com/b/web-155417042.jpg","me":"https://www.youngernation.com/wp-content/uploads/2017/12/Meghalaya-1.jpg","mh":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Maharashtra.jpg","mn":"https://www.youngernation.com/wp-content/uploads/2017/12/Manipur-1.jpg","mp":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Madhya-Pradesh.jpg",'ml':'https://www.youngernation.com/wp-content/uploads/2017/12/Meghalaya-1.jpg',"mz":"https://www.youngernation.com/wp-content/uploads/2017/12/Mizoram-1.jpg","nl":"https://www.youngernation.com/wp-content/uploads/2017/12/Nagaland-1.jpg","or":"https://www.youngernation.com/wp-content/uploads/2017/12/Odisha.jpg","pb":"https://www.youngernation.com/wp-content/uploads/2017/12/Punjab-1.jpg","py":"https://www.youngernation.com/wp-content/uploads/2017/12/Puducherry.jpg","rj":"https://www.youngernation.com/wp-content/uploads/2017/12/Rajasthan.jpg","sk":"https://www.youngernation.com/wp-content/uploads/2017/12/Sikkim-1.jpg","tg":"https://www.youngernation.com/wp-content/uploads/2017/12/Telangana-1.jpg","tn":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-Tamil-Nadu.jpg","tr":"https://www.youngernation.com/wp-content/uploads/2017/12/Tripura-1.jpg",'tt':'https://fvmstatic.s3.amazonaws.com/maps/m/IN-EPS-02-4001.png',"up":"https://www.youngernation.com/wp-content/uploads/2017/12/Uttar-Pradesh.jpg","ut":"https://www.youngernation.com/wp-content/uploads/2017/12/Uttarakhand-1.jpg","wb":"https://www.youngernation.com/wp-content/uploads/2017/12/Indian-State-West-Bengal.jpg"}
namesDict ={'an':'Andaman And Nicobar','ap': 'Andhra Pradesh','ar' :'Arunachal Pradesh','as'  : 'Assam','br' :'Bihar','ch': 'Chandigarh','ct' :'Chattisgarh','dd': 'Daman & Diu','dl' :'Delhi','dn' : 'Dardar and Nagar Haveli','ga': 'Goa','gj' :'Gujarath','hp' :'Himachal Pradesh','hr' : 'Haryana','jh' :'Jarkhand','jk': 'Jammu And Kashmir','ka': 'Karnataka','kl': 'Kerala','ld' : 'Ladakh','la': 'Lakshwadeep','mh': 'Maharashtra','me': 'Meghalaya','ml':'Meghalaya','mn': 'Manipur','mp' : 'Madhya Pradesh','mz': 'Mizoram','nl': 'Nagaland','or': 'Orissa','pb': 'Punjab','py' :'Pondicherry','rj': 'Rajasthan','sk': 'Sikkim','tg': 'Telangana','tn': 'TamilNadu','tt':'India','tr' :'Tripura','up' :'UttarPradesh','ut': 'Uttarakand','wb' :'WestBengal','tt': 'Total'}

li=['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bolivia (Plurinational State of)', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'China, Hong Kong SAR', 'China, Macao SAR', 'China, mainland', 'China, Taiwan Province of', 'Colombia', 'Congo', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', "Democratic People's Republic of Korea", 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'United Republic of Tanzania', 'United States of America', 'Uruguay', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe']
s_names=[ 'Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Daman & Diu', 'Delhi','Dardar and Nagar Haveli', 'Goa', 'Gujarath', 'Himachal Pradesh','Haryana', 'Jarkhand', 'Jammu And Kashmir', 'Karnataka', 'Kerala','Ladakh', 'Lakshwadeep', 'Maharashtra', 'Meghalaya', 'Manipur','Madhya Pradesh', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab','Pondicherry', 'Rajasthan', 'Sikkim', 'Telangana', 'TamilNadu','Tripura', 'UttarPradesh', 'Uttarakand', 'WestBengal', 'India']
s_keys={'an':'Andaman and Nicobar Islands', 'ap':'Andhra Pradesh', 'ar':'Arunachal Pradesh', 'as':'Assam', 'br':'Bihar', 'ch':'Chhattisgarh', 'ct':'Chandigarh', 'dd':'Daman and Diu', 'dl':'Delhi', 'dn':'Dadra and Nagar Haveli', 'ga':'Goa', 'gj':'Gujarat', 'hp':'Himachal Pradesh', 'hr':'Haryana', 'jh':'Jharkhand', 'jk':'Jammu and Kashmir', 'ka':'Karnataka', 'kl':'Kerala', 'la':'Ladakh', 'ld':'Lakshadweep', 'mh': 'Maharashtra', 'ml':'Meghalaya', 'mn':'Manipur', 'mp':'Madhya Pradesh', 'mz':'Mizoram', 'nl':'Nagaland', 'or':'Odisha', 'pb':'Punjab', 'py':'Puducherry', 'rj':'Rajasthan', 'sk':'Sikkim', 'tg':'Telangana', 'tn':'Tamil Nadu', 'tr':'Tripura','up':'Uttar Pradesh', 'ut':'Uttarakhand', 'wb':'West Bengal'}
stateDict={'an': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fan.png?alt=media',
 'ap': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fap.png?alt=media',
 'ar': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Far.png?alt=media',
 'as': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fas.png?alt=media',
 'br': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fbr.png?alt=media',
 'ch': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fch.png?alt=media',
 'ct': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fct.png?alt=media',
 'dd': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fdd.png?alt=media',
 'dl': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fdl.png?alt=media',
 'dn': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fdn.png?alt=media',
 'ga': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fga.png?alt=media',
 'gj': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fgj.png?alt=media',
 'hp': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fhp.png?alt=media',
 'hr': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fhr.png?alt=media',
 'jh': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fjh.png?alt=media',
 'jk': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fjk.png?alt=media',
 'ka': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fka.png?alt=media',
 'kl': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fkl.png?alt=media',
 'la': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fla.png?alt=media',
 'ld': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fld.png?alt=media',
 'mh': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fmh.png?alt=media',
 'ml': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fml.png?alt=media',
 'mn': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fmn.png?alt=media',
 'mp': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fmp.png?alt=media',
 'mz': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fmz.png?alt=media',
 'nl': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fnl.png?alt=media',
 'or': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2For.png?alt=media',
 'pb': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fpb.png?alt=media',
 'py': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fpy.png?alt=media',
 'rj': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Frj.png?alt=media',
 'sk': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fsk.png?alt=media',
 'tg': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Ftg.png?alt=media',
 'tn': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Ftn.png?alt=media',
 'tr': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Ftr.png?alt=media',
 'tt': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Ftt.png?alt=media',
 'up': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fup.png?alt=media',
 'ut': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fut.png?alt=media',
 'wb': 'https://firebasestorage.googleapis.com/v0/b/brave-theater-255512.appspot.com/o/states%2Fwb.png?alt=media'}
if __name__=='__main__':
	app.run()
