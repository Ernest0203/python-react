import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const generateLine = (data : any) => {
  return [...data].sort((a, b) => a.x - b.x)
}

type ScatterPanelProps = {
  title: string;
  data: { x: number; y: number }[];
  xLabel: string;
  yLabel: string;
};

const ScatterPanel = ({ title, data, xLabel, yLabel }: ScatterPanelProps) => {
  const line = generateLine(data)

  return (
    <div className="w-full h-72 bg-white rounded-lg shadow p-4 mb-6">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart>
          <CartesianGrid />
          <XAxis dataKey="x" name={xLabel} label={{ value: xLabel, position: 'insideBottomRight', offset: -5 }} />
          <YAxis dataKey="y" name={yLabel} label={{ value: yLabel, angle: -90, position: 'insideLeft' }} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name={title} data={data} fill="#82ca9d" />
          <Scatter
            name="Линия тренда"
            data={line}
            line={{ stroke: "#ff7300", strokeWidth: 2 }}
            fill="none"
            shape={() => null} // Скрыть точки линии
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}

type AnalyzeScatterProps = {
  result: {
    charts?: {
      salary_vs_experience?: { salary: number; years_experience: number }[];
      salary_vs_age?: { salary: number; age: number }[];
    };
  };
};

const AnalyzeScatter = ({ result }: AnalyzeScatterProps) => {
  const salaryExp = result.charts?.salary_vs_experience?.map(d => ({
    x: d.years_experience,
    y: d.salary,
  })) || [];

  const salaryAge = result.charts?.salary_vs_age?.map(d => ({
    x: d.age,
    y: d.salary,
  })) || [];

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Scatter графики</h2>
      <ScatterPanel title="Зарплата vs Опыт" data={salaryExp} xLabel="Опыт (лет)" yLabel="Зарплата" />
      <ScatterPanel title="Зарплата vs Возраст" data={salaryAge} xLabel="Возраст" yLabel="Зарплата" />
    </div>
  );
};

export default AnalyzeScatter;
