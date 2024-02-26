# Backend - Trivia API

## Documenting your Endpoints

The following provides detailed documentation of the backend API endpoints including the URL, request parameters, and the response body.

- [Backend - Trivia API](#backend---trivia-api)
  - [Documenting your Endpoints](#documenting-your-endpoints)
    - [Categories Endpoints](#categories-endpoints)
      - [`GET '/api/v1.0/categories'`](#get-apiv10categories)
      - [`GET /api/v1.0/categories/<int:categoryId>'`](#get-apiv10categoriesintcategoryid)
      - [`GET /api/v1.0/categories/<int:categoryId>/questions'`](#get-apiv10categoriesintcategoryidquestions)
    - [Questions Endpoints](#questions-endpoints)
      - [`GET '/api/v1.0/questions'`](#get-apiv10questions)
      - [`TODO GET '/api/v1.0/questions/category'`](#todo-get-apiv10questionscategory)
      - [`GET '/api/v1.0/questions/random'`](#get-apiv10questionsrandom)
      - [`POST '/api/v1.0/questions'`](#post-apiv10questions)
      - [`POST '/api/v1.0/questions/search'`](#post-apiv10questionssearch)
      - [`DELETE '/api/v1.0/questions/<int:question_id>'`](#delete-apiv10questionsintquestion_id)


### Categories Endpoints

#### `GET '/api/v1.0/categories'`

- Fetches an array of category objects in which the ids are the categories ids and the type is the corresponding string of the category
- Request Arguments: None
- Usage example: `http://127.0.0.1:5000/api/v1.0/categories` 
- Returns: An object with a key, `data`, that contains an array of objects with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "data": [
        {   "id": 1, "type": "Science" },
        {   "id": 2, "type": "Art" },
        {   "id": 3, "type": "Geography" },
        {   "id": 4, "type": "History" },
        {   "id": 5, "type": "Entertainment" },
        {   "id": 6, "type": "Sports" }
    ],
    "success": true
}
```
---

#### `GET /api/v1.0/categories/<int:categoryId>'`

- Fetches a category object in with Id and the corresponding string of the category
- Request Arguments: the ID as integer of the category requested
- Usage example: `http://127.0.0.1:5000/api/v1.0/categories/1` 
- Returns: An object with a key, `data`, that contains an object with  `id: key, type: string` attributes, and a `success` boolean key.

```json
{
    "data": { "id": 1, "type": "Science" },
    "success": true
}
```
- if the category is not found it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```
---

#### `GET /api/v1.0/categories/<int:categoryId>/questions'`

- Fetches the questions belonging to the specified category
- Request Arguments: the ID as integer of the category requested
- Usage example: `http://127.0.0.1:5000/api/v1.0/categories/1/questions` 
- Returns: A 200 (OK) status and an object with a `category` object with  `id: key, type: string` attributes, a `data` array containing the question objects with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, and a `success` boolean flag.

```json
{
    "category": { "id": 1, "type": "Science" },
    "data": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true
}
```
- if the category is not found it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```
---

### Questions Endpoints

#### `GET '/api/v1.0/questions'`

- Fetches the questions belonging to the specified category
- Request Arguments: 
  - `category`: the ID as integer of the category requested
  - perPage: the number of question per page to be returned
  - page: the page of questions to be returned
- Usage example: `http://127.0.0.1:5000/api/v1.0/questions?page=1&category=1&perPage=2` 
- Returns an object with:
  - a `categories` array of category object with  `id: key, type: string` attributes, 
  - a `category` object with  `id: key, type: string` attributes or null, 
  - a `data` array containing the question objects with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, 
  - a `page` integer key value pair indicating the current page (defaults to 1), 
  - a `pages` integer key value pair indicating the number of pages available,
  - a `perPage` integer key value pair indicating the number of questions per page (defaults to 10),
  - a `total` integer key value pair indicating the total number of questions available,
  - and a `success` boolean flag.

```json
{
    "categories": [
        { "id": 1, "type": "Science" },
        { "id": 2, "type": "Art" },
        ...
    ],
    "category": null,
    "data": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        ...
    ],
    "page": 1,
    "pages": 2,
    "perPage": 10,
    "success": true,
    "total": 19
}

```
- if the category is not found it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```

- if the page is not found it returns a status of 404 (not found) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Database error. Page outside limits.",
    "message": "Not found",
    "success": false
}
```

---

#### `TODO GET '/api/v1.0/questions/category'`
- Fetches the questions belonging to the specified category
- This endpoint performs the same function of `GET /api/v1.0/categories/<int:categoryId>/questions'` only under the question endopint for convenience 
- Request Arguments: 
  - either the ID as integer of the category requested OR
  - the type as string of the category requested
- Usage example 
  - `http://127.0.0.1:5000/api/v1.0/questions/category?id=1` OR
  - `http://127.0.0.1:5000/api/v1.0/questions/category?type=science`
- Returns: A 200 (OK) status and an object with a `category` object with  `id: key, type: string` attributes, a `data` array containing the question objects with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, and a `success` boolean flag.

```json
{
    "category": { "id": 1, "type": "Science" },
    "data": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true
}
```
- if no id or type are submitted or if both are submitted it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Bad category arguments. Submit either category Id or type",
    "message": "Unprocessable entity",
    "success": false
}
```

- if the category is not found it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```
---

#### `GET '/api/v1.0/questions/random'`
- Fetches a random question from the entire pool of avaliable questions or from a specific category if specified in the body of the request. It keeps track of the questiuons already returned to avoid returning the same question twice.
- Request Arguments: 
  - none
- Request Body:
  - a json object containing a `category:int or null` key:value pair  and a `previous: [int]` containing the ids of previously fetched questions  
- Usage example `http://127.0.0.1:5000/api/v1.0/questions/random`
```json
{
    "category": null,
    "previous":[26, 20]
}
```
- Returns a 200 (OK) status and an object with 
  - an `available:int` key:value pair indicating howmayn more questions are available in the pool, 
  - a `category: string|null` key:value pair indicating the current category of questions if any, 
  - a `data` object containing a question object with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, 
  - a `previous: [int]` containing the ids of previously fetched questions  
  - and a `success` boolean flag. 
```json
{
    "available": 17,
    "category": null,
    "data": {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    "previous": [
        26,
        20,
        14
    ],
    "success": true
}
```

- if the category is invalid it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```

- if the previous array containd invalid data it returns a status of 500 (internal server error) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "(psycopg2.errors.InvalidTextRepresentation)...",
    "message": "Internal Server Error",
    "success": false
}
```
---

#### `POST '/api/v1.0/questions'`
- Insert a question
- Request Arguments: 
  - none
- Request Body:
  - a json object with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes  
  - `difficulty` defaults to 0 if omitted
- Usage example `http://127.0.0.1:5000/api/v1.0/questions`
```json
{
    "question": "Do you like python?",
    "answer": "Duuuuhh!!",
    "category": 1,
    "difficulty": 10
}
```
- Returns a 200 (OK) status and an object with a `data` object containing the question inserted with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, and a `success` boolean flag.
```json
{
    "data": {
        "answer": "Duuuuhh!!",
        "category": 1,
        "difficulty": 10,
        "id": 25,
        "question": "Do you like python?"
    },
    "success": true
}

- if the category is not found it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Category does not exist",
    "message": "Unprocessable entity",
    "success": false
}
```

- if the question or answer are missing or empty it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Invalid data [question or answer]",
    "message": "Unprocessable entity",
    "success": false
}
```
---

#### `POST '/api/v1.0/questions/search'`
- Fetches a list of questions where the search term is a substring of the field question 
- Request Arguments: 
  - none
- Request Body:
  - a json key:value pair  with  `search: value` attributes  
```json
{
    "search": "title",
}
```
- Usage example `http://127.0.0.1:5000/api/v1.0/questions/search`
- Returns a 200 (OK) status and an object with a `data` object containing a list of questions with  `id: key, category: key, difficulty: int, question: string, answer: string ` attributes, a `found:int` value indicating how may questions matched the query, a `query:string` value returning the query text,  and a `success` boolean flag. 
```json
{
    "data": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "found": 2,
    "query": "title",
    "success": true
}
```
- If a valid search is submitted but no records are found  `e.g: "search": "titlez" or "search": " "` it will return a 200 (OK) status and a json object as described above with the 'data' field as an empty array and found will be `0`
```json
{
    "data": [],
    "found": 0,
    "query": "titlez",
    "success": true
}
```

- if the body is empty or does not contain a valid search key:value pair it returns a status of 422 (unprocessable entity) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "No search string provided",
    "message": "Unprocessable entity",
    "success": false
}
```
---

#### `DELETE '/api/v1.0/questions/<int:question_id>'`
- Deletes the question specified by the ID
- Request Arguments: 
  - `id`: the ID as integer of the category requested
- Returns a 200 (OK) status and a `Question #<ID> has been successfully deleted.` content message  if successful
- Usage example `http://127.0.0.1:5000/api/v1.0/questions/25`
- if the question is not found it returns a status of 404 (not found) and a json content object with the `error` string, the html status `message` string, and a boolean `success` flag set to false
```json
{
    "error": "Question # <ID> not found.",
    "message": "Not found",
    "success": false
}
```
---
