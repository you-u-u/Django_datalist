import React from "react";

const DataTable = ({ columns, data }) => {
  return (
    <table border="1">
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.length > 0 ? (
          data.map((row, index) => (
            <tr key={index}>
              {columns.map((col) => (
                <td key={col.key}>{row[col.key]}</td>
              ))}
            </tr>
          ))
        ) : (
          <tr><td colSpan={columns.length}>該当するデータがありません。</td></tr>
        )}
      </tbody>
    </table>
  );
};

export default DataTable;
