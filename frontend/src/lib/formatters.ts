export function formatCompactNumber(number: number): string {
  if (number === null || number === undefined) return "N/A";

  const formatter = Intl.NumberFormat("en", {
    notation: "compact",
    maximumFractionDigits: 1,
  });

  return formatter.format(number);
}

export function formatFullNumber(number: number): string {
  if (number === null || number === undefined) return "N/A";

  return new Intl.NumberFormat("en").format(number);
}
