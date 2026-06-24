"""Chart

A declarative, CSS-first, responsive charts. Built using Chart.js.

Composition:
    Use the following composition to build a Chart:

    Chart

Requires:
    Chart.js
"""

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
                "chartInstance": None,
                "_colorCtx": None,
                "_refreshTimer": None,
                "chartConfig": Statement(
                    chart_config.model_dump_json(exclude_none=True),
                    seq_type="assignment",
                ),
                # Expects value to be "var(--name)" or "var(--name) / opacity".
                # Non-var strings are returned unchanged.
                "__resolveColor(value)": Statement(
                    r"""{
                        const match = value.match(/var\((--[\w-)]+)\)(?:\s*\/\s*([\d.]+))?$/);
                        if (!match) return value;

                        const raw = getComputedStyle(document.body).getPropertyValue(match[1]).trim();
                        if (!raw) return value;

                        if (!this._colorCtx) {
                            const canvas = document.createElement('canvas');
                            canvas.width = canvas.height = 1;
                            this._colorCtx = canvas.getContext('2d', { willReadFrequently: true });
                        }

                        this._colorCtx.clearRect(0, 0, 1, 1);
                        this._colorCtx.fillStyle = raw;
                        this._colorCtx.globalAlpha = match[2] ? parseFloat(match[2]) : 1;
                        this._colorCtx.fillRect(0, 0, 1, 1);

                        const[r, g, b, a] = this._colorCtx.getImageData(0, 0, 1, 1).data;
                        return `rgba(${r},${g},${b},${(a / 255).toFixed(3)})`;
                    }""",
                    seq_type="definition",
                ),
                "callbackRegistry": Statement("{ }", seq_type="assignment"),
                "__resolveCallback(value)": Statement(
                    "{ return this.callbackRegistry[value] || value;  }",
                    seq_type="definition",
                ),
                "__resolveConfig(config)": Statement(
                    r"""{
                        if (typeof config === 'string') {
                            if (config.includes('var(--')) {
                                return this.__resolveColor(config);
                            }
                            return config;
                        }

                        if (typeof config !== 'object' || config === null) return config;

                        if (Array.isArray(config)) return config.map(item => this.__resolveConfig(item));

                        return Object.fromEntries(
                            Object.entries(config).flatMap(([key, value]) => {
                            if (typeof value === 'string' && value.startsWith('ALPINE_CALLBACK_')) {
                                const resolvedCallback = this.__resolveCallback(value);

                                if (resolvedCallback === value) {
                                    console.warn(`[Alpine Chart] Missing callback handler for placeholder: "${value}". Skipping key: "${key}".`);
                                    return [];
                                }

                                onst alpineCtx = this;
                                const colorResolvedCallback = function(...args) {
                                    const result = resolvedCallback.apply(this, args);

                                    if (typeof result === 'string' && result.includes('var(--')) {
                                        return alpineCtx.__resolveColor(result);
                                    }
                                    return result;
                                };

                                return [[key, colorResolvedCallback]];
                            }

                                return [[key, this.__resolveConfig(value)]];
                            })
                        );
                    }""",
                    seq_type="definition",
                ),
                "initChart()": Statement(
                    r"""{
                        const canvas = this.$refs.canvas;
                        if (!canvas || typeof Chart === 'undefined') return;

                        Chart.getChart(canvas)?.destroy();

                        this.chartInstance = new Chart(
                            canvas.getContext('2d'), this.__resolveConfig(this.chartConfig)
                        );
                    }""",
                    seq_type="definition",
                ),
                "refreshChart()": Statement(
                    r"""{
                        clearTimeout(this._refreshTimer);
                        this._refreshTimer = setTimeout(() => { this.initChart(); }, 50);
                    }""",
                    seq_type="definition",
                ),
                "updateChartData(newData)": Statement(
                    r"""{
                        if (!this.chartInstance) return;

                        this.chartInstance.data = newData;
                        this.chartInstance.update();
                    }""",
                    seq_type="definition",
                ),
            },
            directive="x-data",
        )
        x_data_attribute = attributes.pop("x_data", None)

        base_x_init_attribute = AlpineJSData(
            data={
                "setup": Statement(
                    r"""() => {
                        $watch('chartConfig', () => refreshChart());
                        $watch('isCurrentThemeDark()', () => refreshChart());
                        $nextTick(() => initChart());
                    }""",
                    seq_type="instance",
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
