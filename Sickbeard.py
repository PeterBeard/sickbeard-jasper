import re
import json
import requests

WORDS = ['TV','EPISODE','SHOW','SOON','DOWNLOAD','SICK','BEARD']


def handle(text, mic, profile):
    """
        Get information about upcoming and recently downloaded TV episodes from Sick Beard

        Arguments:
        text -- transcribed speech input
        mic  -- user I/O object
        profile -- configuration information from Jasper
    """

    # Return False if Sick Beard isn't configured
    if 'sickbeard' in profile:
        SB_HOSTNAME=profile['sickbeard']['host']
        SB_PORT=profile['sickbeard']['port']
        SB_API_KEY=profile['sickbeard']['api_key']
    else:
        mic.say('It looks like you haven\'t configured Sick Beard. See the README for details on how to do this.')
        return False

    base_url = 'http://%s:%s/api/%s/' % (
        SB_HOSTNAME,
        SB_PORT,
        SB_API_KEY
    )

    # Get episodes airing soon
    if 'soon' in text:
        request_url = base_url + '?cmd=future&sort=date&type=soon'

        # Get upcoming episodes from the API
        response = requests.get(request_url)
        json_response = json.loads(response.text)
        
        shows = []
        for show in json_response['data']['soon']:
            shows.append(show['show_name'])

        if len(shows) == 1:
            message = 'There is an episode of %s airing soon.' % shows[0]
        elif len(shows) > 1:
            message = 'There are episodes of %s and %s airing soon.' % (', '.join(shows[:-1]), shows[-1])
        else:
            message = 'It doesn\'t look like any shows have episodes airing soon.'
    # Get recent downloads
    else:
        request_url = base_url + '?cmd=history&limit=5&type=downloaded'

        # Get upcoming episodes from the API
        response = requests.get(request_url)
        json_response = json.loads(response.text)
        
        shows = []
        for show in json_response['data']:
            shows.append(show['show_name'])

        if len(shows) == 1:
            message = 'Sick Beard recently downloaded an episode of %s' % shows[0]
        elif len(shows) > 1:
            message = 'Sick Beard recently downloaded episodes of %s and %s.' % (', '.join(shows[:-1]), shows[-1])
        else:
            message = 'It doesn\'t look like Sick Beard has recently downloaded anything.'

    mic.say(message)
    return True
        
    

def isValid(text):
    """
        Returns True if the input is something we can handle and False otherwise

        Arguments:
        text -- transcribed speech input
    """
    return bool(re.search(r'\b(?:tv|show(s)?|episode(s)?|soon|download|sick|beard)\b', text, re.IGNORECASE))
