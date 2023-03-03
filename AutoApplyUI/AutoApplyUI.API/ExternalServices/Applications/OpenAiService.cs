using System.Text;
using System.Text.Json;

namespace AutoApplyUI.API.ExternalServices.Applications;

public class OpenAiService
{
    public async Task<string> WriteCoverLetter(string posting)
    {
        var x = new Request();
        x.prompt =
            $"Please write a full page cover letter for the following job posting in the language of the posting: \n{posting}";
        var y = JsonSerializer.Serialize(x);
        var client = new HttpClient();
        var request = new HttpRequestMessage
        {
            RequestUri = new Uri("https://api.openai.com/v1/completions"),
            Method = HttpMethod.Post,
            Headers = {
                { "Authorization", $"Bearer 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" }
            },
            Content = new StringContent(y, Encoding.UTF8, "application/json")
        };
        var response = await client.SendAsync(request);
        var application = await response.Content.ReadAsStringAsync();
        return application;
    }

    public class Request
    {
        public string model { get; set; } = "text-davinci-003";
        public string prompt { get; set; } = "Please write a full page cover letter for the following job posting in the language of the posting:";
        public int max_tokens { get; set; } = 2700;
        public float temperature { get; set; } = 0;
        public float top_p { get; set; } = 1;
    }
}
