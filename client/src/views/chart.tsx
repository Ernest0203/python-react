import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'

type ChartPanelProps = {
  label: string;
  data: number[];
}

const ChartPanel = ({ label, data }: ChartPanelProps) => {
  // Преобразуем массив чисел в формат { index, value } для recharts
  const chartData = data.map((value, index) => ({ index, value }))

  console.log("chartData", chartData)

  return (
    <div className="w-full h-64 bg-white rounded-lg shadow p-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="index" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#8884d8" name={label} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartPanel
