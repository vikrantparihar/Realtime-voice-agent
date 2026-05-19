from database.db import (
    get_connection
)


def save_session(
    session_id,
    session
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO sessions (

            session_id,
            full_name,
            dob,
            pan,
            address,
            transcript,
            status

        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,

            session[
                "slots"
            ][
                "full_name"
            ],

            session[
                "slots"
            ][
                "dob"
            ],

            session[
                "slots"
            ][
                "pan"
            ],

            session[
                "slots"
            ][
                "address"
            ],

            "\n".join(
                session[
                    "history"
                ]
            ),

            "ACTIVE"
        )
    )

    conn.commit()

    conn.close()