import re 


def param_extract(response, level, black_list, placeholder):
    """
    Extract URL parameters from response text and replace values with placeholders.

    Args:
        response (str): HTML/text response to parse for URLs with parameters
        level (str): Depth of parameter extraction ('high' extracts nested params)
        black_list (list): List of strings to exclude from results
        placeholder (str): String to replace parameter values with

    Returns:
        list: Unique URLs with parameter values replaced by placeholder

    Uses regex patterns:
        - r'.*?:\/\/.*\?.*\=[^$]' : Matches URLs with at least one parameter
        - r'.*?:\/\/.*\?.*\=' : Basic URL parameter pattern
    """

    ''' 
    regexp : r'.*?:\/\/.*\?.*\=[^$]'
    regexp : r'.*?:\/\/.*\?.*\='
    '''

    parsed = list(set(re.findall(r'.*?:\/\/.*\?.*\=[^$]' , response)))
    final_uris = []
        
    for i in parsed:
        delim = i.find('=')
        second_delim = i.find('=', delim + 1)
        if len(black_list) > 0:
            words_re = re.compile("|".join(black_list))
            if not words_re.search(i):
                final_uris.append((i[:delim+1] + placeholder))
                if level == 'high':
                    final_uris.append(i[:second_delim+1] + placeholder)
        else:
            final_uris.append((i[:delim+1] + placeholder))
            if level == 'high':
                final_uris.append(i[:second_delim+1] + placeholder)

    # for i in final_uris:
    #     k = [ele for ele in black_list if(ele in i)]
    
    return list(set(final_uris))