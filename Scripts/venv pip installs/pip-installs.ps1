﻿#May need to run set-executionpolicy remotesigned in an elevated powershell terminal

#May need to change the below to match your directory
#Builds venv for 
CMD /C "cd C:\repos\CM2305-Voting-System-Prototype-\Voting_System"

CMD /C "py -m venv venv"

CMD /C "venv\Scripts\activate"

CMD /C "pip install -r requirements.txt"

#Builds the venv for admin service

CMD /C "cd C:\repos\CM2305-Voting-System-Prototype-\Admin_Microservice"

CMD /C "py -m venv venv"

CMD /C "venv\Scripts\activate"

CMD /C "pip install -r C:\repos\CM2305-Voting-System-Prototype-\Admin_Microservice\requirements.txt"


# SIG # Begin signature block
# MIIFZwYJKoZIhvcNAQcCoIIFWDCCBVQCAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUZo0UauB/wSvWPQmubRIWeZXK
# HLqgggMEMIIDADCCAeigAwIBAgIQetzlqksqA41HXlytKYfndDANBgkqhkiG9w0B
# AQUFADAYMRYwFAYDVQQDDA1SaHlzQ29ubm9yIFBTMB4XDTE5MTEyMTE5NTc0NVoX
# DTIwMTEyMTIwMTc0NVowGDEWMBQGA1UEAwwNUmh5c0Nvbm5vciBQUzCCASIwDQYJ
# KoZIhvcNAQEBBQADggEPADCCAQoCggEBALY0hjBdhU77MGMR9xHczkbRDIuJXGFX
# XJ1BWPzfkouNjNXnN5+ShTPfcEA7/XT2JxFZxCR2brWFFIbvFMHRrBlBKn1LtJxt
# muDbOV+sf9hZbA0GeUwkjBfd50Mby6Ssr4RfWv1CH3JmS07RPRccPnNyOOe+NLjV
# bv+nZWExYc2ZtBIWB8zaxFugp1khWUZg/7fuxvBRsitMaPJh64ExYy4z7wbI+18M
# JKVM0y9mp1YQsy8wvHtAIPaP2WXdfoAQPt/dSuTUT9eEGfOXH1lOmJQkxSHsakh5
# ZlWgdpA7zpRo98ggMdzkx9GlLpigsM8njya9HXvfyFAm4aNPwS3SS/kCAwEAAaNG
# MEQwDgYDVR0PAQH/BAQDAgeAMBMGA1UdJQQMMAoGCCsGAQUFBwMDMB0GA1UdDgQW
# BBR/OBrhGngW7/RxtpYW2++pdGTahjANBgkqhkiG9w0BAQUFAAOCAQEAp4m0n/t9
# WSuvXCGMtPnQwdwjjLTRpsPoMdM9jwAiUQALww1J/GdDgTW9+GQYC9IQ1ZhGiWP5
# wssslR88bjASziWVeccVgSXY4aNXcahP+7JNvAgZK/T0yRBY0XJ7N/JH40vQWuux
# gC37ZbbZXDX4xIdhFWpa/EA3gKAaN8dRuqnZzxyIkOEjUvcvgPI3HIcc6SWTlZN0
# auaLmPh4Q4UD5BK4maOXTN4x2f9ywpTNzq4JnLdJvebBQdjgiEWZykuXNkuQhvDT
# 6EjS9hQGyW4kb+Qu2Ub44AhA9peJvqyJxi0m84nRfTuMCJOH6nLQbQlkVEx+dkNN
# dE8Pu+lTr8tXujGCAc0wggHJAgEBMCwwGDEWMBQGA1UEAwwNUmh5c0Nvbm5vciBQ
# UwIQetzlqksqA41HXlytKYfndDAJBgUrDgMCGgUAoHgwGAYKKwYBBAGCNwIBDDEK
# MAigAoAAoQKAADAZBgkqhkiG9w0BCQMxDAYKKwYBBAGCNwIBBDAcBgorBgEEAYI3
# AgELMQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQUYezWx/ANYPMDlOlu
# a6/7Y/yvTTQwDQYJKoZIhvcNAQEBBQAEggEAXG0UzF7Cu/1KJhm/kLSSq6izHNwW
# 7xYTCXqJh5XkU0ztHg1wgfP/FRWvd9aratHYUvxolOO/BwaB9T8Di8QVZeLntBiI
# wceAhhPupE0kqOipv/qDi+RJpflXG1ZNRCRZes7/FvqyFfQa+8LkgIAO2Pb4LwV2
# cA9Bdnl1NHWT1245o0e7UXmR3h2LjQ2aaHk+zrzMrI7Mzg54oJGQiPgqcpbHNVTp
# T/O+58PTSHHA/SVjmvYSoWnCbazVBImiWYaLFpj0GJNFB5Jp2RyR5iUl7jgLhDeH
# IMY9PeNKIoh9rVxvTRETBnyvDgA7saU/KgLS5C3H9IZYSVZxBHj+Q+bsAA==
# SIG # End signature block
