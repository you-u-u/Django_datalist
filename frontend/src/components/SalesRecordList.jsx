import React, { useState } from "react";

const SalesRecordList = () => {
  const [records, setRecords] = useState([]); // データ一覧
  const [search, setSearch] = useState("");   // あいまい検索
  const [startDate, setStartDate] = useState(""); // 開始日
  const [endDate, setEndDate] = useState(""); // 終了日
  const [category, setCategory] = useState(""); // カテゴリ
  const [loading, setLoading] = useState(false); // ローディング状態
  const [searched, setSearched] = useState(false); // 検索ボタンを押したか

  // API からデータを取得する関数
  const fetchData = async () => {
    setLoading(true); // ローディング開始
    setSearched(true); // 検索実行フラグを true にする
    try {
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (startDate) params.append("start_date", startDate);
      if (endDate) params.append("end_date", endDate);
      if (category) params.append("category", category);

      const response = await fetch(`http://localhost:8000/api/sales/?${params.toString()}`);
      if (!response.ok) throw new Error("データ取得エラー");

      const data = await response.json();
      setRecords(data);
    } catch (error) {
      console.error("データ取得エラー:", error);
    } finally {
      setLoading(false); // ローディング終了
    }
  };

  return (
    <div>
      <h2>販売記録一覧</h2>

      {/* 検索フォーム */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="商品/モデル/販売経路で検索"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">すべて</option>
          <option value="PC">PC</option>
          <option value="SE品">SE品</option>
        </select>
        <button onClick={fetchData}>検索</button>
      </div>

      {/* 検索ボタンが押されていない場合は何も表示しない */}
      {!searched ? (
        <p>検索条件を入力し、「検索」ボタンを押してください。</p>
      ) : loading ? (
        <p>データ取得中...</p>
      ) : records.length > 0 ? (
        <table border="1">
          <thead>
            <tr>
              <th>販売経路</th>
              <th>商品</th>
              <th>モデル</th>
              <th>区分</th>
              <th>購入日</th>
              <th>購入数</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{record.channel}</td>
                <td>{record.product}</td>
                <td>{record.model}</td>
                <td>{record.category}</td>
                <td>{record.purchase_date}</td>
                <td>{record.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>該当するデータがありません。</p>
      )}
    </div>
  );
};

export default SalesRecordList;
