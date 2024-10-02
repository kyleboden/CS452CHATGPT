import json
from openai import OpenAI
import os
import sqlite3
from time import time, sleep

from python_sql_lite.schema import sql_create_person_table, sql_create_education_table, sql_create_work_experience_table
from query import select_from_table
from db import create_connection

DATABASE = "./pythonsqlite.db"

print("Running bot.py!")

fdir = os.path.dirname(__file__)


def getPath(fname):
    return os.path.join(fdir, fname)


sqliteCon = sqlite3.connect(DATABASE)  # create new db
sqliteCursor = sqliteCon.cursor()


def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result


# OPENAI
configPath = getPath("auth.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key=config["openaiKey"],
    organization=config["orgID"]
)


def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result


setupSqlScript = sql_create_person_table + "\n" + sql_create_education_table + "\n" + sql_create_work_experience_table + "\n"

# strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not expalin it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript +
                                  " Will we have a problem texting any of the people? " +
                                  " \nSELECT p.PersonID, p.FirstName, p.LastName\nFROM Person p WHERE p.Phone IS NULL;\n " +
                                  commonSqlOnlyRequest)
}

questions = [
    "What people have at least one year of work experience?",
    "What people have finished their education?",
    "What is the most popular degree?",
    "What are the different schools in the database?",
    "Is there anyone in the database that has worked in the same job as someone else?",
    "What person has the longest summary?",
    "Who has the most work experience?",
    "Will we have a problem texting any of the people?"
    # "I need insert sql into my tables can you provide good unique data?"
]


def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value


for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question + "\" and the response was \"" + queryRawResponse + "\" Please, just give a concise response in a more friendly way? Please do not give any other suggestions or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })
        sleep(1)

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)

sqliteCursor.close()
sqliteCon.close()
print("Done!")