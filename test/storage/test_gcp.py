import asyncio

import pytest

from openwpm.storage.cloud_storage.gcp_storage import GcsStructuredProvider
from openwpm.storage.storage_providers import TableName
from openwpm.types import VisitId
from test.storage.test_values import TEST_VALUES, TEST_VISIT_IDS


@pytest.mark.skip
@pytest.mark.asyncio
async def test_gcp_structured(mp_logger):
    project = "senglehardt-openwpm-test-1"
    bucket_name = "openwpm-test-bucket"
    structured_provider = GcsStructuredProvider(
        project=project,
        bucket_name=bucket_name,
        base_path="test/2",
        token="/home/stefan/.config/gcloud/legacy_credentials/szabka@mozilla.com/adc.json",
    )
    await structured_provider.init()

    for table_name, test_data in TEST_VALUES.items():
        visit_id = VisitId(test_data["visit_id"])
        await structured_provider.store_record(
            TableName(table_name), visit_id, test_data
        )
    finalize_token = [
        await structured_provider.finalize_visit_id(i) for i in TEST_VISIT_IDS
    ]
    await structured_provider.flush_cache()
    for token in finalize_token:
        await token
