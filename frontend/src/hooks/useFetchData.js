import { useState, useEffect } from "react";

const useFetchData = (url, params) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setSearched(true);
    try {
      const query = new URLSearchParams(params).toString();
      const response = await fetch(`${url}?${query}`);
      if (!response.ok) throw new Error("データ取得エラー");
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("データ取得エラー:", error);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, searched, fetchData };
};

export default useFetchData;
