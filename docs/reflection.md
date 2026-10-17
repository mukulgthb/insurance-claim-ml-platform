Self-Assessment — Phase 0

Overall assessment

My background is in cloud and DevOps engineering. This assignment helped me connect that experience to the application-level workflow of training a model, saving its fitted state, and exposing predictions through an API.



With step-by-step guidance, I implemented a local service using synthetic insurance-claims data, a scikit-learn Pipeline, and FastAPI. I verified training, artifact loading, direct inference, request validation, and model reuse. All 12 automated API tests passed.



My main development priority is independence. I can execute and validate a guided implementation, but I need a deeper understanding of the code and underlying concepts to explain, modify, troubleshoot, and recreate the workflow without detailed assistance.



Three technical development gaps

1\. Python-based training and data workflows

I need to understand how Python code, dependencies, datasets, and algorithms work together to produce a fitted model.



My learning priorities include:



Understanding how dependencies are selected and recorded.



Choosing an appropriate initial model for a defined problem.



Generating synthetic data and loading existing datasets.



Identifying features and target labels.



Understanding what happens during fit() and which parameters are learned.



Separating training from evaluation and interpreting the results.



My goal is to adapt a training workflow to a different dataset independently rather than only execute a prepared example.



2\. API architecture and the inference lifecycle

I need a stronger understanding of how a Python inference function becomes an HTTP service.



I want to trace the complete request path: the server receives a request, FastAPI selects the endpoint, Pydantic validates the payload, the serving code constructs the feature table, and the loaded model generates a prediction.



I also need to understand how to identify the accepted payload, maintain feature compatibility, handle errors, and distinguish startup-time initialization from request-time execution.



My goal is to write and debug a model-serving API independently, including identifying whether a failure originates in the request, application code, model artifact, or runtime environment.



3\. Model internals, serialization, and versioning

I need a concrete understanding of what a trained model contains in memory and what is saved in a .pkl or .joblib artifact.



I want to inspect preprocessing statistics, classifier parameters, metadata, and serialized bytes, and understand how the loaded object uses library code to make predictions. I also need to understand artifact trust, dependency compatibility, and the difference between a model artifact and a standalone application.



For versioning, I want to move beyond a manually assigned label and understand how an immutable artifact can be traced to its training code, dataset, environment, and evaluation results.



Design-help reflection

What I was building

I was building a local service that accepts synthetic insurance-claim details and returns a manual-review prediction using a saved scikit-learn Pipeline.



The project required a complete but minimal workflow: generate synthetic data, train and evaluate a classifier, save the fitted artifact, load it separately, and expose predictions through a validated REST API.



What decision I needed help with

I needed guidance on how to divide responsibilities between training code, the saved artifact, model-loading code, and the API.



In particular, I needed help deciding:



What should happen during training versus inference.



What information should be saved in the artifact.



How preprocessing should remain consistent between training and serving.



When the application should load the model.



How incoming JSON should be converted into model features.



How to validate the implementation rather than assume it worked because the server started.



What I learned

1\. Training and serving should have separate responsibilities

I learned to treat training and inference as separate workflows rather than combine them into one script or endpoint.



In my implementation, training/train.py generates the synthetic dataset, creates the training and test split, fits the Pipeline, evaluates it, and saves the artifact. The serving application then uses that saved result to make predictions.



This helped me understand why a prediction request should not trigger training. The API’s responsibility is to apply an existing fitted model to new input, not recreate the model for every request.



2\. Understanding the scripts requires tracing their execution line by line

I developed an initial understanding of how the training and serving files connect. I need to deepen this by explaining not only what each block does, but also what objects it creates, what data it receives, and what it returns.



For training/train.py, the execution sequence is:



Imports make the required library functions and classes available.



Constants define paths, feature names, and the model-version label.



generate\_data() creates the synthetic feature table and target labels.



train\_test\_split() separates training examples from held-out evaluation examples.



Pipeline(...) constructs the preprocessing and classifier stages.



pipeline.fit(...) fits those stages using the training data.



Prediction and metric calculations evaluate the fitted Pipeline on the test data.



The metadata dictionary records the training context and results.



joblib.dump(...) writes the fitted Pipeline and metadata to the artifact.



For serving, I need to follow two connected files:



app/model.py defines how the artifact is located, loaded, checked, and used. Its prediction method creates an ordered feature table and calls the fitted Pipeline.



app/main.py defines the request and response schemas, initializes the model service during startup, exposes the endpoints, and passes validated input to the prediction method.



This line-by-line approach helps me distinguish defining a function or class from executing it. It also gives me a practical way to investigate failures: identify the current execution stage, inspect its inputs, and check the next operation.



3\. The artifact is the handoff between training and serving

I learned that the training script and the trained artifact are different deliverables. The script describes how the model is created; the artifact preserves the fitted objects and metadata produced by that process.



In this project, the artifact contains the fitted Pipeline and metadata such as feature names, the decision threshold, model version, environment information, and evaluation metrics. The serving code loads these objects rather than importing and executing the training workflow.



This gave me a clearer understanding of how training and serving can operate separately while sharing a defined model artifact.



4\. Inspecting the fitted objects makes the model less of a black box

I learned that understanding the artifact requires looking beyond its filename and examining the objects it contains.



The inspection approach for this project is to load the trusted artifact, access its pipeline and metadata entries, and then examine the Pipeline’s individual stages.



For the fitted scaler, the relevant values include:



mean\_: the learned mean for each input feature.



var\_: the learned variance for each feature.



scale\_: the scaling factors applied during transformation.



For the classifier, the relevant values include:



coef\_: the learned feature coefficients.



intercept\_: the learned intercept.



classes\_: the class labels associated with prediction outputs.



The metadata provides the surrounding context: expected feature names, model version, threshold, training timestamp, dependency information, and evaluation results.



Inspecting these values is a next step in consolidating my understanding. I want to connect each feature to its scaler statistics and classifier coefficient, then follow one example through preprocessing and prediction.



I also want to distinguish inspecting the loaded model from inspecting the artifact bytes. A hexadecimal view shows the file’s byte-level representation, while a serialization disassembly can expose reconstruction instructions. Neither should be confused with a readable listing of the training algorithm.



My objective is to connect these levels clearly:



text





Training source code

&#x20;       ↓

Fitted Python objects and learned values

&#x20;       ↓

Serialized artifact bytes

&#x20;       ↓

Reconstructed objects used for inference

5\. Preprocessing is part of the prediction workflow

I learned that saving only the classifier would leave part of the prediction process outside the artifact.



My implementation saves the fitted StandardScaler and LogisticRegression together in a Pipeline. This keeps the preprocessing used during inference aligned with the preprocessing learned during training.



I now understand the purpose of packaging them together. My next step is to inspect the fitted values and work through a transformation manually so that I understand the calculations, not just the Pipeline interface.



6\. Model loading belongs in application initialization

I learned to load the artifact during the FastAPI application’s startup lifecycle and reuse the resulting ModelService for subsequent requests.



This separates initialization work from prediction work. It also makes a missing artifact a startup problem rather than a failure discovered only when the first prediction request arrives.



I validated that repeated requests reuse the same model service and Pipeline objects. This helped me connect the architecture decision to an observable test rather than treating it only as a coding convention.



7\. The API contract and model feature contract are distinct

I learned that the API accepts a structured JSON request, while the model operates on an ordered feature table.



Pydantic defines the required fields, types, and accepted ranges at the HTTP boundary. The model-serving code then constructs a DataFrame in the expected feature order before invoking the Pipeline.



This clarified why incoming JSON key order should not determine feature order. I tested reordered input keys and confirmed that the prediction remained unchanged.



It also clarified where to find the accepted request payload: in the API’s request schema and interactive documentation, rather than assuming the artifact alone defines the HTTP interface.



8\. Validation must cover behavior, not just successful startup

I learned that a running server is only the beginning of validation. I also need evidence that valid requests succeed, invalid requests are rejected, and the HTTP prediction agrees with direct inference.



The automated tests checked health, prediction structure, invalid inputs, missing and extra fields, feature ordering, model reuse, and latency headers. All 12 tests passed.



This gave me a structured way to demonstrate that the service behaves as intended, while recognizing that these tests do not establish production readiness or real-world model quality.



9\. Implementation success and conceptual mastery are different

I completed a working implementation with guidance, but I should not confuse that result with independent mastery.



The project has given me a concrete system to study. I can now use it to trace execution, inspect fitted state, investigate serialization, modify the input contract, and repeat the workflow with an existing dataset.



I also learned to describe limitations explicitly: the service is local and unauthenticated, the model version is a manually assigned label, and the evaluation uses synthetic data.

