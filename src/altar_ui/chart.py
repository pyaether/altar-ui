import warnings
from typing import Self

from aether.plugins.alpinejs import AlpineJSData, Statement, alpine_js_data_merge
from aether.plugins.chartjs import build_chart_config_from_attributes
from aether.plugins.tailwindcss import tw_merge
from aether.tags.html import Canvas, Div, DivAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035


class Chart(Div):
    def __init__(self, **attributes: Unpack[DivAttributes]):
        base_class_attribute = "relative w-full"
        class_attribute = attributes.pop("_class", "")

        chart_attributes = {
            key: attributes.pop(key)
            for key in list(attributes.keys())
            if key.startswith("chart_")
        }

        chart_config = build_chart_config_from_attributes(
            chart_attributes=chart_attributes
        )

        base_x_data_attribute = AlpineJSData(
            data={
                "chart_instance": None,
                "chart_config": Statement(
                    chart_config.model_dump_json(exclude_none=True),
                    seq_type="assignment",
                ),
                "__resolveCSSVariablesFromConfig(raw_config)": Statement(
                    r"""{
                        if (typeof raw_config !== 'object' || raw_config === null) return raw_config;

                        if (Array.isArray(raw_config)) {
                          return raw_config.map(item => this.__resolveCSSVariablesFromConfig(item));
                        }

                        const resolved_config = {};
                        for (const [key, value] of Object.entries(raw_config)) {
                            if (typeof value === 'string' && value.includes('var(--')) {
                                // Match `var(--variable) / opacity` or just `var(--variable)`
                                const match = value.match(/var\((--[^)]+)\)(?:\s*\/\s*([\d.]+))?/);
                                if (match) {
                                    const variableName = match[1];
                                    const opacity = match[2] ? parseFloat(match[2]) : 1;

                                    let color = getComputedStyle(document.documentElement).getPropertyValue(variableName).trim();

                                    if (opacity < 1) {
                                        if (color.includes('oklch')) {
                                            const oklchMatch = color.match(/oklch\(([\d.]+%?)\s+([\d.]+)\s+([\d.]+)\)/);
                                            if (oklchMatch) {
                                                color = `oklch(${oklchMatch[1]} ${oklchMatch[2]} ${oklchMatch[3]} / ${opacity})`;
                                            }
                                        } else if (color.includes('hsl')) {
                                            const hslMatch = color.match(/hsl\(([\d.]+)\s+([\d.]+)%\s+([\d.]+)%\)/);
                                            if (hslMatch) {
                                                color = `hsla(${hslMatch[1]} ${hslMatch[2]}% ${hslMatch[3]}% / ${opacity})`;
                                            }
                                        } else if (color.includes('rgb')) {
                                            const rgbMatch = color.match(/rgb\(([\d.]+)\s+([\d.]+)\s+([\d.]+)\)/);
                                            if (rgbMatch) {
                                                color = `rgba(${rgbMatch[1]} ${rgbMatch[2]} ${rgbMatch[3]} / ${opacity})`;
                                            }
                                        } else if (color.startsWith('#')) {
                                            const hex = color.slice(1);
                                            const r = parseInt(hex.slice(0, 2), 16);
                                            const g = parseInt(hex.slice(2, 4), 16);
                                            const b = parseInt(hex.slice(4, 6), 16);
                                            color = `rgba(${r}, ${g}, ${b}, ${opacity})`;
                                        }
                                    }
                                    resolved_config[key] = color;
                                } else {
                                    resolved_config[key] = value;
                                }
                            } else if (typeof value === 'object') {
                                resolved_config[key] = this.__resolveCSSVariablesFromConfig(value);
                            } else {
                                resolved_config[key] = value;
                            }
                        }

                        return resolved_config;
                    }""",
                    seq_type="definition",
                ),
                "initChart()": Statement(
                    r"""{
                        const canvas = this.$refs.canvas;
                        if (canvas && typeof Chart !== 'undefined') {
                            const ctx = canvas.getContext('2d');
                            const colorResolvedChartConfig = this.__resolveCSSVariablesFromConfig(this.chart_config);
                            console.log(colorResolvedChartConfig)
                            this.chart_instance = new Chart(ctx, colorResolvedChartConfig);
                        }
                    }""",
                    seq_type="definition",
                ),
                "destroyChart()": Statement(
                    r"{ if (this.chart_instance) { this.chart_instance.destroy(); this.chart_instance = null; } }",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        base_x_init_attribute = AlpineJSData(
            data={
                "initialize_chart": Statement(
                    "$nextTick(() => initChart())", seq_type="instance"
                )
            },
            directive="x-init",
        )
        x_init_attribute = attributes.pop("x_init", None)

        super().__init__(
            _class=tw_merge(base_class_attribute, class_attribute),
            x_data=alpine_js_data_merge(base_x_data_attribute, x_data_attribute),
            x_init=alpine_js_data_merge(base_x_init_attribute, x_init_attribute),
            data_slot="chart",
            **attributes,
        )

        self.children = [
            Canvas(_class="w-full h-full", data_slot="chart-canvas", x_ref="canvas")
        ]

    def __call__(self, *_children: tuple) -> Self:
        warnings.warn(
            f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
            UserWarning,
            stacklevel=2,
        )

        return self
