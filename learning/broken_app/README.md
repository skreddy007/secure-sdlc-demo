# Broken lab — excluded from main CI on purpose.
# Use these steps when you want to *see scanners fail*:

# 1) Secret scan
#    gitleaks detect --source learning/broken_app --no-git -v

# 2) SAST
#    semgrep --config p/python --config p/flask learning/broken_app

# 3) SCA (dependencies)
#    trivy fs --severity-source CRITICAL,HIGH learning/broken_app

# 4) Container (after building)
#    docker build -t notes-broken ./learning/broken_app
#    trivy image --severity CRITICAL,HIGH notes-broken
