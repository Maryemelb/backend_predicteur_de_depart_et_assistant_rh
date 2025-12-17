


from fastapi import APIRouter


router= APIRouter(
    tags='predict'
)

router.post('/predict')
def predict():
    