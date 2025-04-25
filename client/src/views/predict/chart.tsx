import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';

type ChartPanelProps = {
  label: string;
  data: number[] | { name: string; value: number }[];
  dataKey?: string;
  nameKey?: string;
};

const ChartPanel = ({ label, data, dataKey = "value", nameKey = "index" }: ChartPanelProps) => {
  const isBarChart = typeof data[0] === "object" && "name" in data[0];

  const formattedData =
    typeof data[0] === "number"
      ? (data as number[]).map((value, index) => ({ index, value }))
      : (data as { name: string; value: number }[]);

  return (
    <div className="w-full h-64 bg-white rounded-lg shadow p-4">
      <ResponsiveContainer width="100%" height="100%">
        {isBarChart ? (
          <BarChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={nameKey} />
            <YAxis />
            <Tooltip />
            <Bar dataKey={dataKey} fill="#82ca9d" name={label} />
          </BarChart>
        ) : (
          <LineChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={nameKey} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey={dataKey} stroke="#8884d8" name={label} />
          </LineChart>
        )}
      </ResponsiveContainer>
    </div>
  );
};

export default ChartPanel;
