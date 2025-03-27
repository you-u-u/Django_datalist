import { useState } from "react";
import useFetchData from "../hooks/useFetchData";
import SearchForm from "../components/SearchForm";
import DataTable from "../components/DataTable";

const Sales = () => {
  const [filters, setFilters] = useState({
    search: "",
    start_date: "",
    end_date: "",
    category: "",
  });

  const { data, loading, searched, fetchData } = useFetchData("http://localhost:8000/api/sales/", filters);

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
  };

  const searchFields = [
    { name: "search", type: "text", placeholder: "商品/モデル/販売経路" },
    { name: "start_date", type: "date" },
    { name: "end_date", type: "date" },
    { name: "category", type: "select", options: ["", "PC", "SE品"] },
  ];

  const tableColumns = [
    { key: "channel", label: "販売経路" },
    { key: "product", label: "商品" },
    { key: "model", label: "モデル" },
    { key: "category", label: "区分" },
    { key: "purchase_date", label: "購入日" },
    { key: "quantity", label: "購入数" },
  ];

  return (
    <div>
      <h2>販売記録一覧</h2>
      <SearchForm fields={searchFields} values={filters} onChange={handleFilterChange} onSearch={fetchData} />
      {loading ? <p>データ取得中...</p> : searched && <DataTable columns={tableColumns} data={data} />}
    </div>
  );
};

export default Sales;
