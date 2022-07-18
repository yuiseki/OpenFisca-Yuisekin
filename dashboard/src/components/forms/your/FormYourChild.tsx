import { useCallback, useContext } from "react";
import { YourselfContext } from "../../../contexts/YourselfContext";

export const FormYourChild = () => {
  const { yourself, setYourself } = useContext(YourselfContext);

  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newYourself = Object.assign(yourself, {
      子どもがいる: event.currentTarget.value === "true" ? true : false,
    });
    setYourself({ ...newYourself });
  }, []);

  return (
    <div className="input-group input-group-lg mb-3">
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="子ども"
          id="子どもはいない"
          value="false"
          checked={
            yourself.子どもがいる === undefined ? false : !yourself.子どもがいる
          }
          onChange={onChange}
        />
        <label className="btn btn-outline-primary" htmlFor="子どもはいない">
          子どもはいない
        </label>
      </div>
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="子ども"
          id="子どもがいる"
          value="true"
          checked={
            yourself.子どもがいる === undefined ? false : yourself.子どもがいる
          }
          onChange={onChange}
        />
        <label className="btn btn-outline-primary" htmlFor="子どもがいる">
          子どもがいる
        </label>
      </div>
    </div>
  );
};
