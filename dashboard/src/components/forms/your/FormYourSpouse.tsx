import { useCallback, useContext } from "react";
import { YourselfContext } from "../../../contexts/YourselfContext";

export const FormYourSpouse = () => {
  const { yourself, setYourself } = useContext(YourselfContext);

  const onChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newYourself = Object.assign(yourself, {
      配偶者がいる: event.currentTarget.value === "true" ? true : false,
    });
    setYourself({ ...newYourself });
  }, []);

  return (
    <div className="input-group input-group-lg mb-3">
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="配偶者"
          id="配偶者はいない"
          value="false"
          checked={
            yourself.配偶者がいる === undefined ? false : !yourself.配偶者がいる
          }
          onChange={onChange}
        />
        <label className="btn btn-outline-primary" htmlFor="配偶者はいない">
          配偶者はいない
        </label>
      </div>
      <div className="form-check-inline">
        <input
          className="btn-check"
          type="radio"
          name="配偶者"
          id="配偶者がいる"
          value="true"
          checked={
            yourself.配偶者がいる === undefined ? false : yourself.配偶者がいる
          }
          onChange={onChange}
        />
        <label className="btn btn-outline-primary" htmlFor="配偶者がいる">
          配偶者がいる
        </label>
      </div>
    </div>
  );
};
