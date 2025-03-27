import React from "react";

const SearchForm = ({ fields, values, onChange, onSearch }) => {
  return (
    <div style={{ marginBottom: "20px" }}>
      {fields.map((field) => (
        <React.Fragment key={field.name}>
          {field.type === "text" && (
            <input
              type="text"
              placeholder={field.placeholder}
              value={values[field.name]}
              onChange={(e) => onChange(field.name, e.target.value)}
            />
          )}
          {field.type === "select" && (
            <select value={values[field.name]} onChange={(e) => onChange(field.name, e.target.value)}>
              {field.options.map((option) => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          )}
          {field.type === "date" && (
            <input
              type="date"
              value={values[field.name]}
              onChange={(e) => onChange(field.name, e.target.value)}
            />
          )}
        </React.Fragment>
      ))}
      <button onClick={onSearch}>検索</button>
    </div>
  );
};

export default SearchForm;
