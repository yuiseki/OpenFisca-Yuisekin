import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [spec, setSpec] = useState<any>();

  useEffect(() => {
    (async () => {
      const newSpecRes = await fetch("http://localhost:50000/spec");
      const newSpecJson = await newSpecRes.json();
      setSpec(newSpecJson);
    })();
  }, []);

  return (
    <div className="App">
      {spec && (
        <>
          <details>
            <summary>世帯</summary>
            <pre>
              {JSON.stringify(spec.definitions["世帯"].properties, null, 2)}
            </pre>
          </details>
          <details>
            <summary>人物</summary>
            <pre>
              {JSON.stringify(spec.definitions["人物"].properties, null, 2)}
            </pre>
          </details>
          <details>
            <summary>エンドポイント</summary>
            <pre>{JSON.stringify(spec.paths, null, 2)}</pre>
          </details>
        </>
      )}
    </div>
  );
}

export default App;
