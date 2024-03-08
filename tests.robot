*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${api_url}    http://127.0.0.1:8000/


*** Test Cases ***
Test Simple Login And Logout
    ${json}    Create Dictionary    email=test@test.com    password=test
    ${response}    POST    ${api_url}login/    json=${json}
    Status Should Be    200    ${response}
    Log    ${response.json()}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${access_token}    Set Variable    ${json['token']}
    ${headers}    Create Dictionary    Content-Type=application/json    Authorization=Token ${access_token}
    ${response}    POST    ${api_url}logout/    headers=${headers}
    Status Should Be    200    ${response}
    ${json}    Convert To Dictionary    ${response.json()}
    ${result}    Set Variable    ${json['success']}
    Should Be Equal As Strings    ${result}    True
    
Test About
    ${json}    Create Dictionary    email=test@test.com    password=test
    ${response}    POST    ${api_url}login/    json=${json}
    Status Should Be    200    ${response}
    Log    ${response.json()}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${access_token}    Set Variable    ${json['token']}
    ${headers}    Create Dictionary    Content-Type=application/json    Authorization=Token ${access_token}
    ${response}    GET    ${api_url}api/description/    headers=${headers}
    Status Should Be    200    ${response}
    ${description}    Set Variable    ${response.json()['description']}
    Log    ${description}
    ${response}    POST    ${api_url}logout/    headers=${headers}
    Status Should Be    200    ${response}
    ${json}    Convert To Dictionary    ${response.json()}
    ${result}    Set Variable    ${json['success']}
    Should Be Equal As Strings    ${result}    True

Test Profile
    ${json}    Create Dictionary    email=test@test.com    password=test
    ${response}    POST    ${api_url}login/    json=${json}
    Status Should Be    200    ${response}
    Log    ${response.json()}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${access_token}    Set Variable    ${json['token']}
    ${headers}    Create Dictionary    Content-Type=application/json    Authorization=Token ${access_token}
    ${response}    GET    ${api_url}api/profile/    headers=${headers}
    Status Should Be    200    ${response}
    ${username}    Set Variable    ${response.json()['username']}
    ${email}    Set Variable    ${response.json()['email']}
    ${sex}    Set Variable    ${response.json()['sex']}
    ${dob}    Set Variable    ${response.json()['dob']}
    Should Be Equal As Strings    ${username}    test
    Should Be Equal As Strings    ${email}    test@test.com
    Should Be Equal As Strings    ${sex}    M
    Should Be Equal As Strings    ${dob}    2024-03-06
    ${response}    POST    ${api_url}logout/    headers=${headers}
    Status Should Be    200    ${response}
    ${json}    Convert To Dictionary    ${response.json()}
    ${result}    Set Variable    ${json['success']}
    Should Be Equal As Strings    ${result}    True

Test Registration
    ${json}    Create Dictionary    username=mariia    email=mariia@gmail.com    password=mariia561286    sex=F
    ...    birthDate=2002-04-14
    ${response}    POST    ${api_url}register/  json=${json}
    Status Should Be    201    ${response}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${id}    Set Variable    ${json['user']['id']}
    ${json}    Create Dictionary    email=mariia@gmail.com    password=mariia561286
    ${response}    POST    ${api_url}login/    json=${json}
    Status Should Be    200    ${response}
    Log    ${response.json()}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${access_token}    Set Variable    ${json['token']}
    ${headers}    Create Dictionary    Content-Type=application/json    Authorization=Token ${access_token}
    ${response}    DELETE    ${api_url}api/users/${id}/    headers=${headers}
    Status Should Be    204    ${response}

Test Main
    ${json}    Create Dictionary    email=test@test.com    password=test
    ${response}    POST    ${api_url}login/    json=${json}
    Status Should Be    200    ${response}
    Log    ${response.json()}
    ${json}    Convert To Dictionary    ${response.json()}
    ${keys_list}    Get Dictionary Keys    ${json}
    ${access_token}    Set Variable    ${json['token']}
    ${headers}    Create Dictionary    Content-Type=application/json    Authorization=Token ${access_token}
    ${params}    Create Dictionary    income=50000    accomodation=1    utilities=40    food=48    transportation=1    
    ...    entertainment=2876    
    ${response}    POST    http://127.0.0.1:8000/api/compute    params=${params}    headers=${headers}
    Status Should Be    200    ${response}
    ${result}    Set Variable    ${response.json()['result']}
    Should Be Equal As Strings    ${result}    success
    ${response}    POST    ${api_url}logout/    headers=${headers}
    Status Should Be    200    ${response}
    ${json}    Convert To Dictionary    ${response.json()}
    ${result}    Set Variable    ${json['success']}
    Should Be Equal As Strings    ${result}    True
