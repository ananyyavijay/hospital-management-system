from fastapi import APIRouter,HTTPException
from psycopg2.extras import RealDictCursor

from db.connection import get_connection

router = APIRouter()

@router.post("", status_code=201)
def create_patient(
    name: str,
    blood_group: str,
    age: int,
    contact: str | None = None
):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT COALESCE(MAX(id), 0) FROM patients
    """)

    count = int(cursor.fetchone()["coalesce"]) + 1
    patient_id = f"P{count:03d}"

    query = """
    INSERT INTO patients(
    patient_id,
        name,
        blood_group,
        age,
        contact
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *;
    """

    cursor.execute(
        query,
        (
            patient_id,
            name,
            blood_group,
            age,
            contact
        )
    )

    patient = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    return patient

@router.get("")
def list_patients(
    blood_group: str | None = None
):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    if blood_group:
        query =  """
        SELECT patient_id, name, blood_group, age, contact 
        FROM patients
        WHERE blood_group = %s
        AND is_active = TRUE
        """

        cursor.execute(query, (blood_group,))

    else:
        query =  """
        SELECT patient_id, name, blood_group, age, contact 
        FROM patients
        WHERE is_active = TRUE
        """
        cursor.execute(query)
    
    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    return patients

@router.get("/{patient_id}")
def get_patient(patient_id: str):

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT patient_id, name, blood_group, age, contact
    FROM patients
    WHERE patient_id = %s
    AND is_active = TRUE
    """
    cursor.execute(query,(patient_id,))

    patient = cursor.fetchone()
    cursor.close()
    connection.close()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient