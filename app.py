import pandas as pd
import requests
from flask import Flask, request, render_template,make_response
app = Flask(__name__)

def verifier(email):
    url ='https://marketjoyemailverifier.azurewebsites.net/up/'+ email
    r=  requests.get(url)
    data = (r.json())
    delivery = data['deliverable'] 
    catch_all = data['catch_all']
    if delivery==True and catch_all==False:
        return 'Valid Email'
    elif delivery==True and catch_all == True:
        return '50:50'
    else:
        return 'Invalid Email'

def e_finder(names,last,domain):
  email= str(names[0][0])+str(last)+'@'+str(domain)# flast@domain.com
  result= verifier(email)
  if result == 'Valid Email':
    return email
  elif result =='Invalid Email':
    email=str(names)+'@'+str(domain)# first@domain.com
    result= verifier(email)
    if result == 'Valid Email':
      return email
    elif result =='Invalid Email':
      email=str(names)+str(last)+'@'+str(domain)# firstlast@domain.com
      result= verifier(email)
      if result == 'Valid Email':
        return email
      elif result== 'Invalid Email':# first.last@domain.com  # fisrtl@domain.com  first.l@domain.com, f_last@domain.com first_l@domain.com
        email = str(names)+'.'+str(last)+'@'+str(domain)
        result = verifier(email)
        if result == 'Valid Email':
          return email
        elif result =='Invalid Email':
          email = str(names)+'_'+str(last)+'@'+str(domain) #first_last@domain.com
          result = verifier(email)
          if result == 'Valid Email':
            return email
          elif result =='Invalid Email':
            email = str(names)+'@'+str(domain) #last@domain.com
            result = verifier(email)
            if result == 'Valid Email':
              return email
            elif result =='Invalid Email':
              email =  str(names[0][0])+'.'+str(last)+'@'+str(domain) #f.last@domain.com
              result = verifier(email)
              if result == 'Valid Email':
                return email
              elif result =='Invalid Email':
                email =  str(names[0][0])+'_'+str(last)+'@'+str(domain) #f_last@domain.com
                result = verifier(email)
                if result == 'Valid Email':
                  return email
                else:
                  return('No valid Email Found')
              else:
                return('No valid Email Found')
            else:
              return('No valid Email Found')
          else:
            return('No valid Email Found')
        else:
          return('No valid Email Found')
      else:
        return('No valid Email Found')
    else:
      return('No valid Email Found')
  else:
    return('No valid Email Found')


@app.route('/verify', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'),encoding='ISO-8859-1',)
        df = pd.DataFrame(df)
        df = df.drop_duplicates()
        df['Status']= df.apply(lambda x: e_finder(x['First'], x['Last'],x['Domain']), axis=1)
        
        
        resp = make_response(df.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=Email_list.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

    return render_template('home.html') 


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=3133)
