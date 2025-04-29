import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'

type PredictionChartProps = {
  actual: number[];
  predicted: number[];
};

const PredictionChart = ({ actual, predicted }: PredictionChartProps) => {
  const chartData = actual.map((value, index) => ({
    index,
    actual: value,
    predicted: predicted[index]
  }));

  return (
    <div className="w-full h-80 bg-white rounded-lg shadow p-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="index" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#8884d8" name="Фактическое" />
          <Line type="monotone" dataKey="predicted" stroke="#82ca9d" name="Предсказанное" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart