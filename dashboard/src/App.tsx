import { useEffect, useState } from "react";
import { OpenFiscaForm } from "./components/form";
import { HouseholdContext } from "./contexts/HouseholdContext";

function App() {
  const yearMonth = `${new Date().getFullYear()}-${new Date().getMonth()}`;
  const [household, setHousehold] = useState({
    世帯員: {
      あなた: {
        誕生年月日: { ETERNITY: undefined },
        所得: {
          [yearMonth]: 0,
        },
      },
    },
    世帯: {
      世帯1: {
        保護者一覧: ["あなた"],
        児童一覧: [],
        児童手当: {
          [yearMonth]: null,
        },
        児童扶養手当: {
          [yearMonth]: null,
        },
        特別児童扶養手当: {
          [yearMonth]: null,
        },
        障害児童育成手当: {
          [yearMonth]: null,
        },
      },
    },
  });
  const householdContextValue = {
    household,
    setHousehold,
  };
  const [spec, setSpec] = useState<any>();

  useEffect(() => {
    (async () => {
      const newSpecRes = await fetch("http://localhost:50000/spec");
      const newSpecJson = await newSpecRes.json();
      setSpec(newSpecJson);
    })();
  }, []);

  return (
    <HouseholdContext.Provider value={householdContextValue}>
      <div className="container">
        <h1>OpenFisca-Yuisekin</h1>
        <hr />
        <div>
          <OpenFiscaForm />
        </div>
        <hr />
        <div>
          <h2>仕様</h2>
          {spec && (
            <>
              <details>
                <summary>世帯</summary>
                <pre>
                  {JSON.stringify(spec.definitions.世帯.properties, null, 2)}
                </pre>
              </details>
              <details>
                <summary>人物</summary>
                <pre>
                  {JSON.stringify(spec.definitions.人物.properties, null, 2)}
                </pre>
              </details>
              <details>
                <summary>エンドポイント</summary>
                <pre>{JSON.stringify(spec.paths, null, 2)}</pre>
              </details>
            </>
          )}
        </div>
      </div>
    </HouseholdContext.Provider>
  );
}

export default App;
