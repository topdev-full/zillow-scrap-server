from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/parse', methods=['GET'])
def parse_url():
    url = f"https://www.zillow.com/homedetails/{request.args.get('id')}_zpid/"
    print(url   )
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    try:
        # Make the request to ZenRows API
        api_key = "6f370a86fa4ce1f13716a1d42fede7a94c8f5e26"
        params = {
            "apikey": api_key,
            "url": url,
            "js_render": "true",
            "antibot": "true",
            "premium_proxy": "true"
        }

        return jsonify({'text': "Back to search Save Share More Off market Street View $15,500 12183 Van Gough Ave, Pt Charlotte, FL 33981 -- beds -- baths -- sqft Loading Unknown Built in ---- -- sqft lot $-- Zestimate \u00ae $--/sqft $6/mo HOA What's special This home is located at 12183 Van Gough Ave, Pt Charlotte, FL 33981. Show more Facts & features Property Lot Size : 10,000 sqft Details Parcel number : 412106333006 Construction Type & style Home type : Unknown Community & neighborhood Location Region : Pt Charlotte HOA & financial HOA Has HOA : Yes HOA fee : $6 monthly Show more Services availability Claim this home Florida Charlotte County Port Charlotte 33981 12183 Van Gough Ave Nearby cities Boca Grande Real estate Englewood Real estate Placida Real estate Port Charlotte Real estate Punta Gorda Real estate Rotonda West Real estate Show more About Zestimates Research Careers Careers - U.S. Privacy Notice Careers - Mexico Privacy Notice Help Advertise Fair Housing Guide Advocacy Terms of use Privacy Notice Cookie Preference Learn AI Mobile Apps Trulia StreetEasy HotPads Out East ShowingTime+ Do Not Sell or Share My Personal Information \u2192 Zillow Group is committed to ensuring digital accessibility for individuals with disabilities. We are continuously working to improve the accessibility of our web experience for everyone, and we welcome feedback and accommodation requests. If you wish to report an issue or seek an accommodation, please let us know . Zillow, Inc. holds real estate brokerage licenses in multiple states. Zillow (Canada), Inc. holds real estate brokerage licenses in multiple provinces. \u00a7 442-H New York Standard Operating Procedures \u00a7 New York Fair Housing Notice TREC: Information about brokerage services , Consumer protection notice California DRE #1522444 Contact Zillow, Inc. Brokerage For listings in Canada, the trademarks REALTOR\u00ae, REALTORS\u00ae, and the REALTOR\u00ae logo are controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA. The trademarks MLS\u00ae, Multiple Listing Service\u00ae and the associated logos are owned by CREA and identify the quality of services provided by real estate professionals who are members of CREA. Used under license. Follow us: Visit us on facebook Visit us on instagram Visit us on tiktok \u00a9 2006 to 2025 Zillow \u00a9 2006-2025 Zillow Equal Housing Opportunity"})
        
        response = requests.get("https://api.zenrows.com/v1/", params=params)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with class "layout-container-desktop"
        target_div = soup.find('div', class_='layout-container-desktop')
        
        if target_div:
            all_text = target_div.get_text(strip=True, separator=' ')
            return jsonify({'text': all_text})
        else:
            return jsonify({'error': 'Could not find div with class layout-container-desktop'}), 404
            
    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8089)
