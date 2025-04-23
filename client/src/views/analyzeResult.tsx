import ChartPanel from './chart'

type Stats = {
  mean?: number;
  min?: number;
  max?: number;
  [key: string]: number | undefined;
};

type AnalyzeResultProps = {
  result: {
    summary: Record<string, Stats>;
  };
};

const AnalyzeResult = ({ result }: AnalyzeResultProps) => {
  const numericColumns = Object.entries(result.summary).filter(
    ([_, stats]) => typeof stats.mean === "number"
  )

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Графики по числовым колонкам</h2>
      {numericColumns.map(([key, stats]) => (
        <div key={key} className="mb-6">
          <h3 className="text-lg mb-2">{key}</h3>
          <ChartPanel
            label={key}
            data={Object.entries(stats)
              .map(([_, val]) => (typeof val === "number" ? val : null))
              .filter((val): val is number => val !== null)}
          />
        </div>
      ))}
    </div>
  )
}

export default AnalyzeResult