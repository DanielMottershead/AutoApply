using System.Text.Json.Serialization;
using Azure;
using Azure.Data.Tables;

namespace AutoApplyUI.API.ExternalServices.Postings
{
    public class PostingsService
    {

        public async Task<List<Posting>> GetPostings()
        {
            var client = new TableClient("DefaultEndpointsProtocol=https;AccountName=jobpostingevents;AccountKey=Ylygnp75H3u/25qzk6X6IfnoFYl90WdNJvefut+d8wwl87oIfB9pWx53dzvWfqX8yLaWdmKC/uyG+ASt3gd84Q==;EndpointSuffix=core.windows.net", "Postings");
            var result = client.Query<JobPostingEntity>();
            return result.ToList().Select(i => i.Map()).ToList();
        }
    }

    public static class PostingMapper
    {
        public static Posting Map(this JobPostingEntity postingEntity)
        {
            return new Posting()
            {
                CompanyName = postingEntity.PartitionKey,
                Description = postingEntity.description,
                JobTitle = postingEntity.job_title,
                SalaryRangeBot = postingEntity.salary_range_low,
                SalaryRangeTop = postingEntity.salary_range_high
            };
        }
    }

    public class Posting
    {
        public string CompanyName { get; set; }
        public int SalaryRangeTop { get; set; }
        public int SalaryRangeBot { get; set; }
        public string JobTitle { get; set; }
        public string Description { get; set; }
    }

    public class JobPostingEntity : ITableEntity
    {
        public string PartitionKey { get; set; }
        public string RowKey { get; set; }
        public DateTimeOffset? Timestamp { get; set; }
        public ETag ETag { get; set; }
        [JsonPropertyName("job_title")]
        public string job_title { get; set; }
        [JsonPropertyName("posted")]
        public string posted { get; set; }
        [JsonPropertyName("salary_range_low")]
        public int salary_range_low { get; set; }
        [JsonPropertyName("salary_range_high")]
        public int salary_range_high { get; set; }
        [JsonPropertyName("link")]
        public string link { get; set; }
        [JsonPropertyName("Description")]
        public string description { get; set; }
    }
}
