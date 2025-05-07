import { useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer
} from "recharts"

const intervals = ["5", "30", "60", "240", "360", "720", "D", "W", "M"]

const CryptoChart = () => {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [interval, setInterval] = useState("60");
  const [days, setDays] = useState(7);
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await axios.get("http://127.0.0.1:8000/crypto/history", {
        params: {
          symbol,
          interval,
          days,
        },
      })

      console.log(res.data)

      // Преобразуем timestamp в читаемую дату
      const chartData = res.data.map((item: any) => ({
        ...item,
        time: new Date(item.timestamp).toLocaleString(),
      }));

      setData(chartData);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4 bg-white shadow rounded-xl space-y-4">
      <div className="flex items-center gap-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          className="border px-2 py-1 rounded w-40"
          placeholder="BTCUSDT"
        />
        <input
          type="number"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="border px-2 py-1 rounded w-40"
          min={1}
        />
        <select
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          {intervals.map((intv) => (
            <option key={intv} value={intv}>
              {intv}
            </option>
          ))}
        </select>
        <button
          onClick={fetchData}
          className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
        >
          Загрузить
        </button>
      </div>

      {loading && <p>Загрузка данных...</p>}

      {!loading && data.length > 0 && (
        <div className="w-full h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" hide />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default CryptoChart
