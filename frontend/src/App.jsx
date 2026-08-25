import { useState } from "react";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const handleSubmit = async (event) => {

    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setResult(null);


    try {

      setLoading(true);

      setError("");


      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: question
          })
        }
      );


      const data = await response.json();


      console.log("API Response:", data);


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to process the question."
        );

      }


      setResult(data);

      setAnswer(data.answer);


    } catch (error) {

      console.error("Error:", error);


      setError(
        error.message ||
        "Unable to connect to the AI Business Analyst."
      );


    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="app">

      <header className="header">

        <h1>AI Business Analyst</h1>

        <p>
          Ask questions about your business data
        </p>

      </header>


      <main className="main">

        <section className="question-section">

          <h2>Ask a business question</h2>

          <form onSubmit={handleSubmit}>

            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Example: Why did revenue drop in February?"
            />


            <div className="examples">

              <p>Try asking:</p>


              <button
                type="button"
                onClick={() =>
                  setQuestion("What is our total revenue?")
                }
              >
                Total revenue
              </button>


              <button
                type="button"
                onClick={() =>
                  setQuestion("Show revenue by month.")
                }
              >
                Revenue trend
              </button>


              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "Why did revenue drop in February?"
                  )
                }
              >
                Revenue decline
              </button>

            </div>


            <button
              type="submit"
              disabled={loading}
            >

              {loading
                ? "Analyzing..."
                : "Analyze"}

            </button>

          </form>

        </section>


        {error && (

          <section className="error-section">

            <p>{error}</p>

          </section>

        )}


        {loading && (

          <section className="answer-section">

            <h2>Analyzing your question...</h2>

            <div className="answer-card">

              <p>
                Generating SQL, analyzing your data,
                and preparing insights...
              </p>

            </div>

          </section>

        )}


        {answer && (

          <section className="answer-section">

            <h2>Business Insight</h2>

            <div className="answer-card">

              <p>{answer}</p>

            </div>

          </section>

        )}


        {result?.chart && (

          <section className="chart-section">

            <h2>Visualization</h2>

            <img
              src={result.chart}
              alt="Business analysis chart"
            />

          </section>

        )}


        {result?.sql && (

          <section className="sql-section">

            <h2>Generated SQL</h2>

            <pre>
              {result.sql}
            </pre>

          </section>

        )}


        {result?.data?.length > 0 && (

          <section className="data-section">

            <h2>Data</h2>

            <pre>
              {JSON.stringify(
                result.data,
                null,
                2
              )}
            </pre>

          </section>

        )}

      </main>

    </div>

  );

}


export default App;