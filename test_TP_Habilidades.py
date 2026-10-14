import contextlib
import io
import unittest
from unittest.mock import Mock, patch

import TP_Habilidades


class MerakiToolTests(unittest.TestCase):
    def test_choose_item_by_id_without_prompting(self):
        items = [
            {"id": "org-1", "name": "Primera"},
            {"id": "org-2", "name": "Segunda"},
        ]

        with patch("builtins.input") as input_mock:
            selected = TP_Habilidades.choose_item(
                items, "una organización", "org-2"
            )

        self.assertEqual(selected["name"], "Segunda")
        input_mock.assert_not_called()

    def test_choose_item_rejects_unknown_id(self):
        items = [{"id": "org-1", "name": "Primera"}]
        with self.assertRaisesRegex(TP_Habilidades.ItemNotFoundError, "ID unknown"):
            TP_Habilidades.choose_item(items, "una organización", "unknown")

    def test_choose_item_rejects_id_when_catalog_is_empty(self):
        with self.assertRaises(TP_Habilidades.ItemNotFoundError):
            TP_Habilidades.choose_item([], "una red", "network-1")

    def test_main_requires_api_key(self):
        stderr = io.StringIO()
        with (
            patch.dict("os.environ", {}, clear=True),
            contextlib.redirect_stderr(stderr),
        ):
            result = TP_Habilidades.main([])

        self.assertEqual(result, 1)
        self.assertIn("MERAKI_DASHBOARD_API_KEY", stderr.getvalue())

    def test_get_json_raises_for_http_error(self):
        session = Mock()
        response = session.get.return_value
        response.raise_for_status.side_effect = TP_Habilidades.requests.HTTPError(
            "unauthorized"
        )

        with self.assertRaises(TP_Habilidades.requests.HTTPError):
            TP_Habilidades.get_json(session, "organizations")

        session.get.assert_called_once_with(
            "https://api.meraki.com/api/v1/organizations", timeout=30
        )


if __name__ == "__main__":
    unittest.main()