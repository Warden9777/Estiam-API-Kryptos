from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from classes.schema_dto import User

router = APIRouter(
    tags=["Auth"],
    prefix='/auth'
)

class LoginData(BaseModel):
    email: str
    password: str

# Définissez le schéma OAuth2 pour la récupération du jeton d'accès
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Endpoint pour l'authentification
@router.post('/login', response_model=dict)
async def login_user(login_data: LoginData):
    # Vérifiez les informations d'authentification (adaptez ceci en fonction de votre base de données d'utilisateurs)
    user = authenticate_user(login_data.email, login_data.password)
    
    if user:
        # Si l'authentification réussit, générer un jeton d'accès (à adapter à vos besoins)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Fonction d'authentification (à adapter à votre logique)
def authenticate_user(email, password):
    # Remplacez ceci par la logique d'authentification réelle (vérification en base de données, etc.)
    # Si l'authentification réussit, retournez l'objet User correspondant, sinon None
    user = None
    if check_user_credentials(email, password):
        user = User(email=email, password=password)
    return user

# Fonction de vérification des informations d'identification (à adapter à votre logique)
def check_user_credentials(email, password):
    # Remplacez ceci par la logique de vérification réelle (base de données, Firebase, etc.)
    # Si les informations d'identification sont correctes, retournez True, sinon False
    return (email == "test@example.com" and password == "password")

# Endpoint protégé pour obtenir les données de l'utilisateur actuel
@router.get('/me')
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user
